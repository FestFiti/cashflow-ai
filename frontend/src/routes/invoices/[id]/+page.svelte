<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';

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

	const statusClasses: Record<string, string> = {
		paid: 'border-emerald-500/20 bg-emerald-500/10 text-emerald-400',
		sent: 'border-blue-500/20 bg-blue-500/10 text-blue-400',
		overdue: 'border-amber-500/20 bg-amber-500/10 text-amber-400',
		draft: 'border-white/[0.08] bg-white/[0.03] text-white/40'
	};

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
			<div class="h-3.5 w-28 rounded bg-white/[0.04]"></div>
			<div class="h-8 w-48 rounded bg-white/[0.04]"></div>
			<div class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-8">
				<div class="h-4 w-64 rounded bg-white/[0.04]"></div>
			</div>
		</div>
	{:else if invoice}
		<!-- Back link -->
		<a href="/invoices" class="mb-6 inline-flex items-center gap-1.5 text-[13px] text-white/25 transition-colors hover:text-white/50">
			<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
			</svg>
			Back to invoices
		</a>

		<!-- Main Card -->
		<div class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6 md:p-8 transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<!-- Header -->
			<div class="flex items-start justify-between">
				<div class="flex items-center gap-4">
					<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-white/[0.03] text-lg font-semibold text-white/30">
						{invoice.client_name.charAt(0)}
					</div>
					<div>
						<h1 class="font-['Instrument_Serif'] text-2xl tracking-tight text-white md:text-3xl">
							{invoice.client_name}
						</h1>
						<div class="mt-1 flex flex-wrap items-center gap-x-3 gap-y-1">
							<span class="text-[12px] text-white/20">{invoice.client_phone}</span>
							{#if invoice.client_email}
								<span class="text-[12px] text-white/20">{invoice.client_email}</span>
							{/if}
						</div>
					</div>
				</div>
				<span class="rounded-full border px-3 py-1 text-[11px] font-medium capitalize {statusClasses[invoice.status] || statusClasses.draft}">
					{invoice.status}
				</span>
			</div>

			<!-- Divider -->
			<div class="my-6 border-t border-white/[0.04]"></div>

			<!-- Details Grid -->
			<div class="grid grid-cols-2 gap-6 md:grid-cols-3">
				<div>
					<p class="text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Amount</p>
					<p class="mt-1.5 font-['Instrument_Serif'] text-3xl italic tracking-tight text-emerald-400">{formatKES(invoice.amount)}</p>
				</div>
				<div>
					<p class="text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Due Date</p>
					<p class="mt-1.5 text-lg font-semibold text-white/80">{new Date(invoice.due_date).toLocaleDateString()}</p>
				</div>
				<div>
					<p class="text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Created</p>
					<p class="mt-1.5 text-lg font-semibold text-white/80">{new Date(invoice.created_at).toLocaleDateString()}</p>
				</div>
			</div>

			<!-- Divider -->
			<div class="my-6 border-t border-white/[0.04]"></div>

			<!-- Description -->
			<div>
				<p class="text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Description</p>
				<p class="mt-2 text-[13px] leading-relaxed text-white/40">{invoice.description}</p>
			</div>

			<!-- Actions -->
			{#if invoice.status !== 'paid'}
				<div class="mt-8 flex gap-3">
					<button
						class="flex flex-1 items-center justify-center gap-2 rounded-xl bg-emerald-500 py-2.5 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400"
					>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3" />
						</svg>
						Send M-Pesa Request
					</button>
					<button
						class="flex items-center gap-2 rounded-xl border border-white/[0.08] px-5 py-2.5 text-[13px] font-medium text-white/40 transition-all hover:border-white/[0.15] hover:text-white/60"
					>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3" />
						</svg>
						Download PDF
					</button>
				</div>
			{/if}
		</div>
	{/if}
</div>
