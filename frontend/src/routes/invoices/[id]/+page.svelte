<script lang="ts">
	import { page } from '$app/stores';
	import { onMount, onDestroy } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { theme } from '$lib/stores/theme';
	import { getAvatarUrl } from '$lib/avatar';
	import { showError, showSuccess } from '$lib/stores/toast';

	const isDark = $derived($theme === 'dark');

	interface InvoiceItem {
		id: string;
		name: string;
		description: string | null;
		quantity: number;
		unit_price: number;
		total: number;
	}

	interface Invoice {
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
	}

	let invoice = $state<Invoice | null>(null);
	let loading = $state(true);
	let visible = $state(false);
	let stkLoading = $state(false);
	let stkMessage = $state('');
	let pollInterval: ReturnType<typeof setInterval> | null = null;
	let linkCopied = $state(false);

	const invoiceNumber = $derived(invoice ? invoice.id.slice(0, 8).toUpperCase() : '');
	const hasItems = $derived(invoice?.items && invoice.items.length > 0);
	const subtotal = $derived(hasItems ? invoice!.items.reduce((sum, item) => sum + item.total, 0) : 0);
	const shareableLink = $derived(invoice ? `${typeof window !== 'undefined' ? window.location.origin : ''}/pay/${invoice.id}` : '');

	const statusClasses = $derived<Record<string, string>>({
		paid: 'border-emerald-500/20 bg-emerald-500/10 text-emerald-400',
		sent: 'border-blue-500/20 bg-blue-500/10 text-blue-400',
		overdue: 'border-amber-500/20 bg-amber-500/10 text-amber-400',
		draft: `${isDark ? 'border-white/[0.08]' : 'border-zinc-200'} ${isDark ? 'bg-white/[0.03]' : 'bg-white'} ${isDark ? 'text-white/40' : 'text-zinc-500'}`
	});

	onMount(async () => {
		if (!$auth.token) { goto('/login'); return; }
		try {
			invoice = await api<Invoice>(`/invoices/${$page.params.id}`, { token: $auth.token });
		} catch {
			goto('/invoices');
		} finally {
			loading = false;
			setTimeout(() => (visible = true), 50);
		}
	});

	onDestroy(() => { if (pollInterval) clearInterval(pollInterval); });

	async function sendMpesaRequest() {
		if (!invoice || stkLoading) return;
		stkLoading = true;
		stkMessage = '';
		try {
			const res = await api<{ checkout_request_id: string; message: string }>(
				'/payments/stk-push',
				{ method: 'POST', body: JSON.stringify({ invoice_id: invoice.id }), token: $auth.token! }
			);
			stkMessage = res.message || 'Check your phone and enter M-Pesa PIN';
			startPolling(res.checkout_request_id);
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to send M-Pesa request');
			stkLoading = false;
		}
	}

	function startPolling(checkoutId: string) {
		let attempts = 0;
		pollInterval = setInterval(async () => {
			attempts++;
			try {
				const res = await api<{ status: string; mpesa_receipt: string | null }>(
					`/payments/${checkoutId}/status`,
					{ token: $auth.token! }
				);
				if (res.status === 'completed') {
					clearInterval(pollInterval!); pollInterval = null; stkLoading = false; stkMessage = '';
					showSuccess(`Payment confirmed! Receipt: ${res.mpesa_receipt}`);
					invoice = await api<Invoice>(`/invoices/${invoice!.id}`, { token: $auth.token! });
				} else if (res.status === 'failed') {
					clearInterval(pollInterval!); pollInterval = null; stkLoading = false; stkMessage = '';
					showError('Payment was cancelled or failed. Please try again.');
				} else if (attempts >= 24) {
					clearInterval(pollInterval!); pollInterval = null; stkLoading = false; stkMessage = '';
					showError('Payment timed out. Check your M-Pesa messages.');
				}
			} catch { /* keep polling */ }
		}, 5000);
	}

	async function copyShareableLink() {
		try {
			await navigator.clipboard.writeText(shareableLink);
			linkCopied = true;
			showSuccess('Link copied to clipboard');
			setTimeout(() => { linkCopied = false; }, 2000);
		} catch {
			showError('Failed to copy link');
		}
	}

	function shareViaWhatsApp() {
		if (!invoice) return;
		const text = encodeURIComponent(`Invoice #${invoiceNumber} for ${formatKES(invoice.amount)}\n\nView and pay here: ${shareableLink}`);
		window.open(`https://wa.me/?text=${text}`, '_blank');
	}
</script>

<svelte:head>
	<title>{invoice ? `Invoice #${invoiceNumber} — ${invoice.client_name}` : 'Invoice'} — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	{#if loading}
		<div class="animate-pulse space-y-4">
			<div class="h-3.5 w-28 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
			<div class="h-8 w-48 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
			<div class="grid grid-cols-12 gap-6">
				<div class="col-span-12 lg:col-span-8 rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-8">
					<div class="h-4 w-64 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
				</div>
				<div class="col-span-12 lg:col-span-4 rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-8">
					<div class="h-4 w-32 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
				</div>
			</div>
		</div>
	{:else if invoice}
		<a href="/invoices" class="mb-4 inline-flex items-center gap-1.5 text-[13px] {isDark ? 'text-white/25' : 'text-zinc-400'} transition-colors {isDark ? 'hover:text-white/50' : 'hover:text-zinc-600'}">
			<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
			</svg>
			Back to invoices
		</a>

		<!-- Invoice Number Header -->
		<div class="mb-6 flex items-center gap-3">
			<h1 class="font-['Instrument_Serif'] text-2xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'} md:text-3xl">
				Invoice <span class="italic text-emerald-400">#{invoiceNumber}</span>
			</h1>
			<span class="rounded-full border px-3 py-1 text-[11px] font-medium capitalize {statusClasses[invoice.status] || statusClasses.draft}">{invoice.status}</span>
		</div>

		<div class="grid grid-cols-12 gap-6 transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<!-- Left Column: Invoice Details -->
			<div class="col-span-12 lg:col-span-8">
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 md:p-8">
					<!-- Client Info -->
					<div class="flex items-center gap-4">
						<img src={getAvatarUrl(invoice.client_name)} alt={invoice.client_name} class="h-12 w-12 rounded-lg" />
						<div>
							<h2 class="text-[15px] font-semibold {isDark ? 'text-white/80' : 'text-zinc-700'}">{invoice.client_name}</h2>
							<div class="mt-0.5 flex flex-wrap items-center gap-x-3 gap-y-1">
								<span class="text-[12px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{invoice.client_phone}</span>
								{#if invoice.client_email}<span class="text-[12px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{invoice.client_email}</span>{/if}
							</div>
						</div>
					</div>

					<div class="my-6 border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-200'}"></div>

					<!-- Amount / Due / Created -->
					<div class="grid grid-cols-2 gap-6 md:grid-cols-3">
						<div>
							<p class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Amount</p>
							<p class="mt-1.5 font-['Instrument_Serif'] text-3xl italic tracking-tight text-emerald-400">{formatKES(invoice.amount)}</p>
						</div>
						<div>
							<p class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Due Date</p>
							<p class="mt-1.5 text-lg font-semibold {isDark ? 'text-white/80' : 'text-zinc-700'}">{new Date(invoice.due_date).toLocaleDateString()}</p>
						</div>
						<div>
							<p class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Created</p>
							<p class="mt-1.5 text-lg font-semibold {isDark ? 'text-white/80' : 'text-zinc-700'}">{new Date(invoice.created_at).toLocaleDateString()}</p>
						</div>
					</div>

					<div class="my-6 border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-200'}"></div>

					<!-- Line Items or Description -->
					{#if hasItems}
						<div>
							<p class="mb-4 text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Line Items</p>
							<div class="overflow-x-auto">
								<table class="w-full">
									<thead>
										<tr class="border-b {isDark ? 'border-white/[0.04]' : 'border-zinc-200'}">
											<th class="pb-3 text-left text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Item</th>
											<th class="pb-3 text-center text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Qty</th>
											<th class="pb-3 text-right text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Unit Price</th>
											<th class="pb-3 text-right text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Total</th>
										</tr>
									</thead>
									<tbody>
										{#each invoice.items as item}
											<tr class="border-b {isDark ? 'border-white/[0.04]' : 'border-zinc-100'}">
												<td class="py-3">
													<p class="text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">{item.name}</p>
													{#if item.description}
														<p class="mt-0.5 text-[12px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{item.description}</p>
													{/if}
												</td>
												<td class="py-3 text-center text-[13px] {isDark ? 'text-white/60' : 'text-zinc-600'}">{item.quantity}</td>
												<td class="py-3 text-right text-[13px] {isDark ? 'text-white/60' : 'text-zinc-600'}">{formatKES(item.unit_price)}</td>
												<td class="py-3 text-right text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">{formatKES(item.total)}</td>
											</tr>
										{/each}
									</tbody>
									<tfoot>
										<tr>
											<td colspan="3" class="pt-4 text-right text-[12px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Subtotal</td>
											<td class="pt-4 text-right text-[14px] font-semibold {isDark ? 'text-white/80' : 'text-zinc-700'}">{formatKES(subtotal)}</td>
										</tr>
									</tfoot>
								</table>
							</div>
						</div>
					{:else}
						<div>
							<p class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Description</p>
							<p class="mt-2 text-[13px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">{invoice.description}</p>
						</div>
					{/if}
				</div>
			</div>

			<!-- Right Column: Actions -->
			<div class="col-span-12 lg:col-span-4 space-y-4">
				<!-- STK Push Loading -->
				{#if stkLoading}
					<div class="rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-5">
						<div class="flex items-center gap-3">
							<div class="h-4 w-4 animate-spin rounded-full border-2 border-emerald-500/30 border-t-emerald-500"></div>
							<div>
								<p class="text-[13px] font-medium text-emerald-400">Waiting for payment...</p>
								{#if stkMessage}<p class="mt-0.5 text-[12px] text-emerald-400/60">{stkMessage}</p>{/if}
							</div>
						</div>
					</div>
				{/if}

				<!-- Payment Status / M-Pesa Button -->
				{#if invoice.status !== 'paid'}
					<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-5">
						<p class="mb-3 text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Payment</p>
						<button
							onclick={sendMpesaRequest}
							disabled={stkLoading}
							class="flex w-full items-center justify-center gap-2 rounded-xl bg-emerald-500 py-2.5 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-50"
						>
							{#if stkLoading}
								<div class="h-4 w-4 animate-spin rounded-full border-2 border-zinc-950/30 border-t-zinc-950"></div>
								Waiting for PIN...
							{:else}
								<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3" />
								</svg>
								Send M-Pesa Request
							{/if}
						</button>
					</div>
				{:else}
					<div class="rounded-2xl border border-emerald-500/20 bg-emerald-500/5 p-5">
						<div class="flex items-center gap-2">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
							</svg>
							<p class="text-[13px] font-medium text-emerald-400">Payment received</p>
						</div>
					</div>
				{/if}

				<!-- Share & Download -->
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-5">
					<p class="mb-3 text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Share & Export</p>
					<div class="space-y-2">
						<button
							onclick={copyShareableLink}
							class="flex w-full items-center gap-2 rounded-xl border {isDark ? 'border-white/[0.08]' : 'border-zinc-200'} px-4 py-2.5 text-[13px] font-medium {isDark ? 'text-white/40' : 'text-zinc-500'} transition-all {isDark ? 'hover:border-white/[0.15]' : 'hover:border-zinc-300'} {isDark ? 'hover:text-white/60' : 'hover:text-zinc-700'}"
						>
							{#if linkCopied}
								<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
								</svg>
								<span class="text-emerald-400">Link Copied!</span>
							{:else}
								<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
									<path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m9.86-1.06a4.5 4.5 0 00-1.242-7.244l-4.5-4.5a4.5 4.5 0 00-6.364 6.364l1.757 1.757" />
								</svg>
								Copy Shareable Link
							{/if}
						</button>
						<button
							onclick={shareViaWhatsApp}
							class="flex w-full items-center gap-2 rounded-xl border {isDark ? 'border-white/[0.08]' : 'border-zinc-200'} px-4 py-2.5 text-[13px] font-medium {isDark ? 'text-white/40' : 'text-zinc-500'} transition-all {isDark ? 'hover:border-white/[0.15]' : 'hover:border-zinc-300'} {isDark ? 'hover:text-white/60' : 'hover:text-zinc-700'}"
						>
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 24 24" fill="currentColor">
								<path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z" />
							</svg>
							Share via WhatsApp
						</button>
						<button class="flex w-full items-center gap-2 rounded-xl border {isDark ? 'border-white/[0.08]' : 'border-zinc-200'} px-4 py-2.5 text-[13px] font-medium {isDark ? 'text-white/40' : 'text-zinc-500'} transition-all {isDark ? 'hover:border-white/[0.15]' : 'hover:border-zinc-300'} {isDark ? 'hover:text-white/60' : 'hover:text-zinc-700'}">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
							</svg>
							Download PDF
						</button>
					</div>
				</div>

				<!-- Invoice Info -->
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-5">
					<p class="mb-3 text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Details</p>
					<div class="space-y-3">
						<div>
							<p class="text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Invoice ID</p>
							<p class="mt-0.5 text-[12px] font-mono {isDark ? 'text-white/40' : 'text-zinc-500'}">{invoice.id}</p>
						</div>
						<div>
							<p class="text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Shareable Link</p>
							<p class="mt-0.5 text-[12px] font-mono {isDark ? 'text-white/40' : 'text-zinc-500'} break-all">/pay/{invoice.id}</p>
						</div>
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>
