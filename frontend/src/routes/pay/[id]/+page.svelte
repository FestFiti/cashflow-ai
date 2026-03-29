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

	// Payment state
	let phone = $state('');
	let paying = $state(false);
	let payError = $state('');
	let payStatus = $state<'idle' | 'pending' | 'completed' | 'failed'>('idle');
	let payMessage = $state('');
	let checkoutId = $state('');
	let pollTimer = $state<ReturnType<typeof setInterval> | null>(null);

	const API_URL = import.meta.env.VITE_API_URL ?? '';

	async function loadInvoice() {
		try {
			const res = await fetch(`${API_URL}/api/invoices/public/${$page.params.id}`);
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
	}

	onMount(() => {
		loadInvoice();
		return () => {
			if (pollTimer) clearInterval(pollTimer);
		};
	});

	async function initiatePayment() {
		if (!phone.trim() || !invoice) return;
		paying = true;
		payError = '';
		payStatus = 'idle';

		try {
			const res = await fetch(`${API_URL}/api/invoices/public/${invoice.id}/pay`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ phone: phone.trim() }),
			});
			const data = await res.json();
			if (!res.ok) {
				payError = data.detail || 'Payment request failed';
				paying = false;
				return;
			}

			payStatus = 'pending';
			payMessage = data.message || 'Check your phone for the M-Pesa prompt';
			checkoutId = data.checkout_request_id;
			paying = false;

			// Start polling
			pollTimer = setInterval(pollPaymentStatus, 5000);
		} catch {
			payError = 'Network error. Please try again.';
			paying = false;
		}
	}

	async function pollPaymentStatus() {
		if (!checkoutId || !invoice) return;
		try {
			const res = await fetch(
				`${API_URL}/api/invoices/public/${invoice.id}/payment-status/${checkoutId}`
			);
			if (!res.ok) return;
			const data = await res.json();

			if (data.status === 'completed') {
				payStatus = 'completed';
				if (pollTimer) clearInterval(pollTimer);
				// Reload invoice to get updated status
				setTimeout(async () => {
					const r = await fetch(`${API_URL}/api/invoices/public/${$page.params.id}`);
					if (r.ok) invoice = await r.json();
				}, 1000);
			} else if (data.status === 'failed') {
				payStatus = 'failed';
				payError = 'Payment was not completed. Please try again.';
				if (pollTimer) clearInterval(pollTimer);
			}
		} catch {
			// Silently retry on next poll
		}
	}

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
	<div class="mx-auto max-w-7xl px-4 py-8 md:px-8 md:py-12">
		{#if loading}
			<div class="grid gap-8 lg:grid-cols-12">
				<div class="lg:col-span-7">
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
				</div>
				<div class="lg:col-span-5">
					<div class="animate-pulse rounded-2xl border border-zinc-200 bg-white p-8 shadow-sm">
						<div class="h-6 w-40 rounded bg-zinc-100"></div>
						<div class="mt-6 h-12 rounded bg-zinc-100"></div>
						<div class="mt-4 h-12 rounded bg-zinc-100"></div>
					</div>
				</div>
			</div>
		{:else if error}
			<div class="mx-auto max-w-lg rounded-2xl border border-zinc-200 bg-white p-12 text-center shadow-sm">
				<div class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-red-50">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
					</svg>
				</div>
				<h2 class="mt-4 font-['Instrument_Serif'] text-xl text-zinc-900">{error}</h2>
				<p class="mt-2 text-[13px] text-zinc-400">This invoice may have been removed or the link is invalid.</p>
			</div>
		{:else if invoice}
			<div class="grid gap-8 lg:grid-cols-12 transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<!-- Left Column: Invoice Document -->
				<div class="lg:col-span-7">
					<div class="rounded-2xl border border-zinc-200 bg-white shadow-sm">
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
					</div>
				</div>

				<!-- Right Column: Payment + Contact -->
				<div class="lg:col-span-5 space-y-6">
					{#if invoice.status === 'paid'}
						<!-- Paid Confirmation Card -->
						<div class="rounded-2xl border border-emerald-200 bg-emerald-50 p-8 text-center shadow-sm">
							<div class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-emerald-100">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
								</svg>
							</div>
							<h3 class="mt-4 font-['Instrument_Serif'] text-2xl italic text-emerald-800">Payment Received</h3>
							<p class="mt-2 text-[14px] text-emerald-700">
								This invoice has been paid in full. Thank you!
							</p>
							<p class="mt-4 text-[24px] font-semibold text-emerald-600">{formatKES(invoice.amount)}</p>
						</div>
					{:else}
						<!-- Payment Card -->
						<div class="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm">
							<h3 class="text-[16px] font-semibold text-zinc-900">Pay with M-Pesa</h3>
							<p class="mt-1 text-[13px] text-zinc-500">
								Enter your M-Pesa phone number to pay <span class="font-semibold text-emerald-600">{formatKES(invoice.amount)}</span>
							</p>

							{#if payStatus === 'completed'}
								<div class="mt-5 rounded-xl border border-emerald-200 bg-emerald-50 p-5 text-center">
									<div class="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-100">
										<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
											<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
										</svg>
									</div>
									<p class="mt-3 text-[14px] font-semibold text-emerald-700">Payment Successful!</p>
									<p class="mt-1 text-[13px] text-emerald-600">Your payment has been received.</p>
								</div>
							{:else}
								<div class="mt-5">
									<label for="phone" class="block text-[12px] font-medium text-zinc-600">Phone Number</label>
									<input
										id="phone"
										type="tel"
										bind:value={phone}
										placeholder="e.g. 0712345678"
										disabled={paying || payStatus === 'pending'}
										class="mt-1.5 w-full rounded-lg border border-zinc-200 bg-zinc-50 px-4 py-3 text-[14px] text-zinc-900 placeholder-zinc-400 outline-none transition-colors focus:border-emerald-300 focus:bg-white focus:ring-2 focus:ring-emerald-100 disabled:opacity-60"
									/>
								</div>

								{#if payError}
									<div class="mt-3 rounded-lg border border-red-100 bg-red-50 px-4 py-3">
										<p class="text-[13px] text-red-600">{payError}</p>
									</div>
								{/if}

								{#if payStatus === 'pending'}
									<div class="mt-4 rounded-lg border border-amber-100 bg-amber-50 px-4 py-4 text-center">
										<div class="mx-auto h-6 w-6 animate-spin rounded-full border-2 border-amber-300 border-t-amber-600"></div>
										<p class="mt-2 text-[13px] font-medium text-amber-700">{payMessage}</p>
										<p class="mt-1 text-[12px] text-amber-500">Waiting for confirmation...</p>
									</div>
								{:else}
									<button
										onclick={initiatePayment}
										disabled={paying || !phone.trim()}
										class="mt-4 w-full rounded-lg bg-emerald-600 px-4 py-3 text-[14px] font-semibold text-white shadow-sm transition-all hover:bg-emerald-700 active:scale-[0.98] disabled:cursor-not-allowed disabled:opacity-50"
									>
										{#if paying}
											<span class="inline-flex items-center gap-2">
												<span class="h-4 w-4 animate-spin rounded-full border-2 border-white/30 border-t-white"></span>
												Processing...
											</span>
										{:else}
											Pay {formatKES(invoice.amount)}
										{/if}
									</button>
								{/if}
							{/if}
						</div>
					{/if}

					<!-- Business Contact Card -->
					<div class="rounded-2xl border border-zinc-200 bg-white p-6 shadow-sm">
						<h3 class="text-[14px] font-semibold text-zinc-900">Contact</h3>
						<div class="mt-3 space-y-2">
							<div class="flex items-center gap-3">
								<div class="flex h-8 w-8 items-center justify-center rounded-lg bg-zinc-100">
									<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
										<path stroke-linecap="round" stroke-linejoin="round" d="M3.75 21h16.5M4.5 3h15M5.25 3v18m13.5-18v18M9 6.75h1.5m-1.5 3h1.5m-1.5 3h1.5m3-6H15m-1.5 3H15m-1.5 3H15M9 21v-3.375c0-.621.504-1.125 1.125-1.125h3.75c.621 0 1.125.504 1.125 1.125V21" />
									</svg>
								</div>
								<div>
									<p class="text-[13px] font-medium text-zinc-700">{invoice.business.name}</p>
									{#if invoice.business.address}
										<p class="text-[12px] text-zinc-400">{invoice.business.address}{invoice.business.city ? `, ${invoice.business.city}` : ''}</p>
									{/if}
								</div>
							</div>
							{#if invoice.business.phone}
								<div class="flex items-center gap-3">
									<div class="flex h-8 w-8 items-center justify-center rounded-lg bg-zinc-100">
										<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
											<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 6.75c0 8.284 6.716 15 15 15h2.25a2.25 2.25 0 002.25-2.25v-1.372c0-.516-.351-.966-.852-1.091l-4.423-1.106c-.44-.11-.902.055-1.173.417l-.97 1.293c-.282.376-.769.542-1.21.38a12.035 12.035 0 01-7.143-7.143c-.162-.441.004-.928.38-1.21l1.293-.97c.363-.271.527-.734.417-1.173L6.963 3.102a1.125 1.125 0 00-1.091-.852H4.5A2.25 2.25 0 002.25 4.5v2.25z" />
										</svg>
									</div>
									<p class="text-[13px] text-zinc-600">{invoice.business.phone}</p>
								</div>
							{/if}
						</div>
					</div>
				</div>
			</div>

			<!-- Branding Footer -->
			<div class="mt-10 text-center">
				<p class="text-[12px] text-zinc-400">
					Powered by <span class="font-semibold text-emerald-500">CashFlow AI</span>
				</p>
			</div>
		{/if}
	</div>
</div>
