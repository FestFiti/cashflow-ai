<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { theme } from '$lib/stores/theme';
	import { showError } from '$lib/stores/toast';

	const isDark = $derived($theme === 'dark');

	interface Payment {
		id: string;
		client_name: string;
		description: string;
		amount: number;
		due_date: string;
	}

	let payments = $state<Payment[]>([]);
	let loading = $state(true);
	let visible = $state(false);

	onMount(async () => {
		if (!$auth.token) { goto('/login'); return; }
		await loadPayments();
		setTimeout(() => (visible = true), 50);
	});

	async function loadPayments() {
		try {
			const res = await api<{ payments: Payment[] }>('/payments/overdue');
			payments = res.payments || [];
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to load payments');
		} finally {
			loading = false;
		}
	}

	async function sendReminder(paymentId: string) {
		try {
			await api('/payments/remind', {
				method: 'POST',
				body: JSON.stringify({
					payment_ids: [paymentId]
				})
			});
			await loadPayments();
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to send reminder');
		}
	}
</script>

<svelte:head>
	<title>Send Reminder — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<!-- Back + Header -->
	<a href="/dashboard" class="mb-6 inline-flex items-center gap-1.5 text-[13px] {isDark ? 'text-white/25' : 'text-zinc-400'} transition-colors {isDark ? 'hover:text-white/50' : 'hover:text-zinc-600'}">
		<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
			<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
		</svg>
		Back to dashboard
	</a>
	<div class="mb-8">
		<p class="mb-1 text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Manage</p>
		<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">
			Send <span class="italic text-emerald-400">Reminders</span>
		</h1>
	</div>

	{#if loading}
		<div class="flex items-center justify-center py-12">
			<div class="h-8 w-8 animate-spin rounded-full border-2 border-emerald-500/30 border-t-emerald-500"></div>
		</div>
	{:else if payments.length === 0}
		<div class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-12 text-center">
			<div class="mx-auto mb-4 h-12 w-12 rounded-full bg-emerald-500/10 p-3">
				<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
					<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75l3 3m0 0l3-3m-3 3V7.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
				</svg>
			</div>
			<h3 class="mb-2 text-lg font-medium {isDark ? 'text-white' : 'text-zinc-900'}">All caught up!</h3>
			<p class="text-zinc-400">No overdue payments to remind about.</p>
			<a href="/dashboard" class="mt-4 inline-flex items-center gap-2 rounded-xl bg-emerald-500 px-6 py-2 text-sm font-medium text-zinc-950 transition-colors hover:bg-emerald-400">
				Return to Dashboard
			</a>
		</div>
	{:else}
		<div class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<div class="mb-6">
				<p class="text-[13px] {isDark ? 'text-white/60' : 'text-zinc-600'}">Overdue payments that need reminders</p>
			</div>

			<div class="space-y-4">
				{#each payments as payment}
					<div class="rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-5 transition-all {isDark ? 'hover:border-white/[0.08]' : 'hover:border-zinc-300'}">
						<div class="flex items-start justify-between">
							<div class="flex-1">
								<h3 class="text-[14px] font-semibold {isDark ? 'text-white/80' : 'text-zinc-700'}">{payment.client_name}</h3>
								<p class="mt-1 text-[12px] {isDark ? 'text-white/40' : 'text-zinc-500'}">{payment.description}</p>
								<div class="mt-3 flex items-center gap-4 text-[11px]">
									<span class="{isDark ? 'text-white/20' : 'text-zinc-400'}">Due: {new Date(payment.due_date).toLocaleDateString()}</span>
									<span class="text-amber-400">
										{Math.ceil((new Date().getTime() - new Date(payment.due_date).getTime()) / (1000 * 60 * 60 * 24))} days overdue
									</span>
								</div>
							</div>
							<div class="text-right">
								<p class="text-lg font-medium {isDark ? 'text-white' : 'text-zinc-900'}">{formatKES(payment.amount)}</p>
								<button
									onclick={() => sendReminder(payment.id)}
									class="mt-2 rounded-lg border border-emerald-500/20 bg-emerald-500/10 px-3 py-1.5 text-[11px] font-medium text-emerald-400 transition-colors hover:bg-emerald-500/20"
								>
									Send Reminder
								</button>
							</div>
						</div>
					</div>
				{/each}
			</div>
		</div>
	{/if}

</div>
