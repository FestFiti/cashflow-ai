<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { formatKES } from '$lib/api';

	interface InvoiceItem {
		id: string;
		name: string;
		description: string | null;
		quantity: number;
		unit_price: number;
		total: number;
	}

	interface PublicInvoice {
		id: string;
		client_name: string;
		client_phone: string;
		client_email: string | null;
		amount: number;
		description: string;
		due_date: string;
		status: string;
		created_at: string;
		items: InvoiceItem[];
		business: {
			name: string;
			phone: string;
			logo_url: string | null;
			address: string | null;
			city: string | null;
		};
	}

	let invoice = $state<PublicInvoice | null>(null);
	let loading = $state(true);
	let error = $state('');
	let visible = $state(false);

	const API_URL = import.meta.env.VITE_API_URL ?? '';

	onMount(async () => {
		try {
			const res = await fetch(`${API_URL}/invoices/public/${$page.params.id}`);
			if (!res.ok) {
				error = res.status === 404 ? 'Invoice not found' : 'Failed to load invoice';
				return;
			}
			invoice = await res.json();
		} catch {
			error = 'Failed to load invoice';
		} finally {
			loading = false;
			setTimeout(() => (visible = true), 50);
		}
	});

	const invoiceNumber = $derived(invoice ? invoice.id.slice(0, 8).toUpperCase() : '');
	const hasItems = $derived(invoice?.items && invoice.items.length > 0);
	const subtotal = $derived(hasItems ? invoice!.items.reduce((sum, item) => sum + item.total, 0) : 0);
</script>

<svelte:head>
	<title>{invoice ? `Invoice #${invoiceNumber} — ${invoice.business.name}` : 'Invoice'} — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=DM+Sans:wght@400;500;600;700&display=swap" rel="stylesheet" />
</svelte:head>

<div class="min-h-screen bg-zinc-50" style="font-family: 'DM Sans', sans-serif;">
	<div class="mx-auto max-w-3xl px-4 py-8 md:px-8 md:py-12">
		{#if loading}
			<div class="animate-pulse rounded-2xl border border-zinc-200 bg-white p-8 shadow-sm">
				<div class="flex justify-between">
					<div class="h-10 w-32 rounded bg-zinc-100"></div>
					<div class="h-8 w-24 rounded bg-zinc-100"></div>
				</div>
				<div class="mt-8 space-y-3">
					<div class="h-4 w-64 rounded bg-zinc-100"></div>
					<div class="h-4 w-48 rounded bg-zinc-100"></div>
				</div>
				<div class="mt-8 h-32 rounded bg-zinc-100"></div>
			</div>
		{:else if error}
			<div class="rounded-2xl border border-zinc-200 bg-white p-12 text-center shadow-sm">
				<div class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-red-50">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
					</svg>
				</div>
				<h2 class="mt-4 font-['Instrument_Serif'] text-xl text-zinc-900">{error}</h2>
				<p class="mt-2 text-[13px] text-zinc-400">This invoice may have been removed or the link is invalid.</p>
			</div>
		{:else if invoice}
			<div class="rounded-2xl border border-zinc-200 bg-white shadow-sm transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<!-- Header -->
				<div class="border-b border-zinc-100 px-6 py-6 md:px-8 md:py-8">
					<div class="flex items-start justify-between">
						<div class="flex items-center gap-4">
							{#if invoice.business.logo_url}
								<img src={invoice.business.logo_url} alt={invoice.business.name} class="h-12 w-12 rounded-xl object-cover" />
							{:else}
								<div class="flex h-12 w-12 items-center justify-center rounded-xl bg-emerald-50 text-lg font-bold text-emerald-600">
									{invoice.business.name.charAt(0)}
								</div>
							{/if}
							<div>
								<h2 class="text-[15px] font-semibold text-zinc-900">{invoice.business.name}</h2>
								{#if invoice.business.address}
									<p class="text-[12px] text-zinc-400">{invoice.business.address}</p>
								{/if}
								{#if invoice.business.city}
									<p class="text-[12px] text-zinc-400">{invoice.business.city}</p>
								{/if}
							</div>
						</div>
						<div class="text-right">
							<h1 class="font-['Instrument_Serif'] text-2xl italic tracking-tight text-zinc-900">INVOICE</h1>
							<p class="mt-1 text-[12px] font-medium text-zinc-400">#{invoiceNumber}</p>
						</div>
					</div>
				</div>

				<!-- Bill To + Details -->
				<div class="border-b border-zinc-100 px-6 py-6 md:px-8">
					<div class="grid grid-cols-2 gap-6">
						<div>
							<p class="text-[11px] font-medium uppercase tracking-[0.12em] text-zinc-400">Bill To</p>
							<p class="mt-2 text-[14px] font-semibold text-zinc-900">{invoice.client_name}</p>
							<p class="mt-0.5 text-[12px] text-zinc-500">{invoice.client_phone}</p>
							{#if invoice.client_email}
								<p class="text-[12px] text-zinc-500">{invoice.client_email}</p>
							{/if}
						</div>
						<div class="text-right">
							<div class="mb-3">
								<p class="text-[11px] font-medium uppercase tracking-[0.12em] text-zinc-400">Due Date</p>
								<p class="mt-1 text-[14px] font-semibold text-zinc-700">{new Date(invoice.due_date).toLocaleDateString('en-KE', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
							</div>
							<div>
								<p class="text-[11px] font-medium uppercase tracking-[0.12em] text-zinc-400">Created</p>
								<p class="mt-1 text-[13px] text-zinc-500">{new Date(invoice.created_at).toLocaleDateString('en-KE', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
							</div>
						</div>
					</div>
				</div>

				<!-- Line Items or Description -->
				<div class="px-6 py-6 md:px-8">
					{#if hasItems}
						<table class="w-full">
							<thead>
								<tr class="border-b border-zinc-100">
									<th class="pb-3 text-left text-[11px] font-medium uppercase tracking-[0.12em] text-zinc-400">Item</th>
									<th class="pb-3 text-center text-[11px] font-medium uppercase tracking-[0.12em] text-zinc-400">Qty</th>
									<th class="pb-3 text-right text-[11px] font-medium uppercase tracking-[0.12em] text-zinc-400">Unit Price</th>
									<th class="pb-3 text-right text-[11px] font-medium uppercase tracking-[0.12em] text-zinc-400">Total</th>
								</tr>
							</thead>
							<tbody>
								{#each invoice.items as item}
									<tr class="border-b border-zinc-50">
										<td class="py-3">
											<p class="text-[13px] font-medium text-zinc-700">{item.name}</p>
											{#if item.description}
												<p class="mt-0.5 text-[12px] text-zinc-400">{item.description}</p>
											{/if}
										</td>
										<td class="py-3 text-center text-[13px] text-zinc-600">{item.quantity}</td>
										<td class="py-3 text-right text-[13px] text-zinc-600">{formatKES(item.unit_price)}</td>
										<td class="py-3 text-right text-[13px] font-medium text-zinc-700">{formatKES(item.total)}</td>
									</tr>
								{/each}
							</tbody>
							<tfoot>
								<tr>
									<td colspan="3" class="pt-4 text-right text-[12px] font-medium uppercase tracking-[0.12em] text-zinc-400">Subtotal</td>
									<td class="pt-4 text-right text-[14px] font-semibold text-zinc-700">{formatKES(subtotal)}</td>
								</tr>
							</tfoot>
						</table>
					{:else}
						<div>
							<p class="text-[11px] font-medium uppercase tracking-[0.12em] text-zinc-400">Description</p>
							<p class="mt-2 text-[13px] leading-relaxed text-zinc-600">{invoice.description}</p>
						</div>
					{/if}
				</div>

				<!-- Total + Status -->
				<div class="border-t border-zinc-100 px-6 py-6 md:px-8">
					<div class="flex items-center justify-between">
						<div class="flex items-center gap-3">
							{#if invoice.status === 'paid'}
								<span class="inline-flex items-center gap-1.5 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1 text-[12px] font-semibold text-emerald-600">
									<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
										<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
									</svg>
									Paid
								</span>
							{:else if invoice.status === 'overdue'}
								<span class="inline-flex items-center gap-1.5 rounded-full border border-amber-200 bg-amber-50 px-3 py-1 text-[12px] font-semibold text-amber-600">
									Overdue
								</span>
							{:else}
								<span class="inline-flex items-center gap-1.5 rounded-full border border-blue-200 bg-blue-50 px-3 py-1 text-[12px] font-semibold text-blue-600 capitalize">
									{invoice.status}
								</span>
							{/if}
						</div>
						<div class="text-right">
							<p class="text-[11px] font-medium uppercase tracking-[0.12em] text-zinc-400">Total Amount</p>
							<p class="mt-1 font-['Instrument_Serif'] text-3xl italic tracking-tight text-emerald-600">{formatKES(invoice.amount)}</p>
						</div>
					</div>
				</div>

				<!-- Payment Section -->
				{#if invoice.status !== 'paid'}
					<div class="border-t border-zinc-100 px-6 py-6 md:px-8">
						<div class="rounded-xl border border-emerald-100 bg-emerald-50/50 p-5">
							<h3 class="text-[14px] font-semibold text-zinc-900">Payment Instructions</h3>
							<p class="mt-2 text-[13px] leading-relaxed text-zinc-600">
								To pay this invoice via M-Pesa, send <span class="font-semibold text-emerald-600">{formatKES(invoice.amount)}</span> to:
							</p>
							<div class="mt-3 rounded-lg bg-white/80 px-4 py-3">
								<p class="text-[12px] font-medium text-zinc-400">Business Name</p>
								<p class="text-[14px] font-semibold text-zinc-900">{invoice.business.name}</p>
								{#if invoice.business.phone}
									<p class="mt-2 text-[12px] font-medium text-zinc-400">M-Pesa Number</p>
									<p class="text-[14px] font-semibold text-zinc-900">{invoice.business.phone}</p>
								{/if}
							</div>
							<p class="mt-3 text-[12px] text-zinc-400">
								Please use invoice reference <span class="font-mono font-semibold text-zinc-600">#{invoiceNumber}</span> when making the payment.
							</p>
						</div>
					</div>
				{/if}
			</div>

			<!-- Branding -->
			<div class="mt-8 text-center">
				<p class="text-[12px] text-zinc-400">
					Powered by <span class="font-semibold text-emerald-500">CashFlow AI</span>
				</p>
			</div>
		{/if}
	</div>
</div>
