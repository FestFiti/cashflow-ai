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
	}

	let invoice = $state<Invoice | null>(null);
	let loading = $state(true);
	let visible = $state(false);
	let stkLoading = $state(false);
	let stkMessage = $state('');
	let pollInterval: ReturnType<typeof setInterval> | null = null;

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
</script>

<svelte:head>
	<title>{invoice ? `Invoice — ${invoice.client_name}` : 'Invoice'} — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-3xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	{#if loading}
		<div class="animate-pulse space-y-4">
			<div class="h-3.5 w-28 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
			<div class="h-8 w-48 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
			<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-8">
				<div class="h-4 w-64 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
			</div>
		</div>
	{:else if invoice}
		<a href="/invoices" class="mb-6 inline-flex items-center gap-1.5 text-[13px] {isDark ? 'text-white/25' : 'text-zinc-400'} transition-colors {isDark ? 'hover:text-white/50' : 'hover:text-zinc-600'}">
			<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
			</svg>
			Back to invoices
		</a>

		<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 md:p-8 transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<div class="flex items-start justify-between">
				<div class="flex items-center gap-4">
					<img src={getAvatarUrl(invoice.client_name)} alt={invoice.client_name} class="h-12 w-12 rounded-lg" />
					<div>
						<h1 class="font-['Instrument_Serif'] text-2xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'} md:text-3xl">{invoice.client_name}</h1>
						<div class="mt-1 flex flex-wrap items-center gap-x-3 gap-y-1">
							<span class="text-[12px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{invoice.client_phone}</span>
							{#if invoice.client_email}<span class="text-[12px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{invoice.client_email}</span>{/if}
						</div>
					</div>
				</div>
				<span class="rounded-full border px-3 py-1 text-[11px] font-medium capitalize {statusClasses[invoice.status] || statusClasses.draft}">{invoice.status}</span>
			</div>

			<div class="my-6 border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-200'}"></div>

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

			<div>
				<p class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Description</p>
				<p class="mt-2 text-[13px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">{invoice.description}</p>
			</div>

			{#if stkLoading}
				<div class="mt-6 rounded-xl border border-emerald-500/20 bg-emerald-500/5 px-4 py-3">
					<div class="flex items-center gap-3">
						<div class="h-4 w-4 animate-spin rounded-full border-2 border-emerald-500/30 border-t-emerald-500"></div>
						<div>
							<p class="text-[13px] font-medium text-emerald-400">Waiting for payment…</p>
							{#if stkMessage}<p class="mt-0.5 text-[12px] text-emerald-400/60">{stkMessage}</p>{/if}
						</div>
					</div>
				</div>
			{/if}

			{#if invoice.status !== 'paid'}
				<div class="mt-8 flex gap-3">
					<button
						onclick={sendMpesaRequest}
						disabled={stkLoading}
						class="flex flex-1 items-center justify-center gap-2 rounded-xl bg-emerald-500 py-2.5 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-50"
					>
						{#if stkLoading}
							<div class="h-4 w-4 animate-spin rounded-full border-2 border-zinc-950/30 border-t-zinc-950"></div>
							Waiting for PIN…
						{:else}
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3" />
							</svg>
							Send M-Pesa Request
						{/if}
					</button>
					<button class="flex items-center gap-2 rounded-xl border {isDark ? 'border-white/[0.08]' : 'border-zinc-200'} px-5 py-2.5 text-[13px] font-medium {isDark ? 'text-white/40' : 'text-zinc-500'} transition-all {isDark ? 'hover:border-white/[0.15]' : 'hover:border-zinc-300'} {isDark ? 'hover:text-white/60' : 'hover:text-zinc-700'}">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
						</svg>
						Download PDF
					</button>
				</div>
			{:else}
				<div class="mt-6 flex items-center gap-2 rounded-xl border border-emerald-500/20 bg-emerald-500/5 px-4 py-3">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
						<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
					</svg>
					<p class="text-[13px] font-medium text-emerald-400">Payment received</p>
				</div>
			{/if}
		</div>
	{/if}
</div>
