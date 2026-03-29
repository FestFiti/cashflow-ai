<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { theme } from '$lib/stores/theme';
	import { showError, showSuccess } from '$lib/stores/toast';
	import { getAvatarUrl } from '$lib/avatar';

	const isDark = $derived($theme === 'dark');

	interface OverdueInvoice {
		id: string;
		client_name: string;
		client_phone: string;
		client_email: string | null;
		description: string;
		amount: number;
		due_date: string;
		status: string;
		is_overdue: boolean;
		days_overdue: number;
	}

	let invoices = $state<OverdueInvoice[]>([]);
	let loading = $state(true);
	let visible = $state(false);
	let sendingId = $state<string | null>(null);

	onMount(async () => {
		if (!$auth.token) { goto('/login'); return; }
		try {
			invoices = await api<OverdueInvoice[]>('/reminders/overdue');
		} catch {
			invoices = [];
		} finally {
			loading = false;
			setTimeout(() => (visible = true), 50);
		}
	});

	async function sendReminder(inv: OverdueInvoice) {
		if (!inv.client_email) {
			showError(`${inv.client_name} has no email address`);
			return;
		}
		sendingId = inv.id;
		try {
			const res = await api<{ message: string }>('/reminders/send', {
				method: 'POST',
				body: JSON.stringify({ invoice_id: inv.id })
			});
			showSuccess(res.message || 'Reminder sent');
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to send reminder');
		} finally {
			sendingId = null;
		}
	}

	const overdueInvoices = $derived(invoices.filter(i => i.is_overdue));
	const pendingInvoices = $derived(invoices.filter(i => !i.is_overdue));
	const totalOverdue = $derived(overdueInvoices.reduce((s, i) => s + i.amount, 0));
</script>

<svelte:head>
	<title>Send Reminders — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<a href="/payments" class="mb-6 inline-flex items-center gap-1.5 text-[13px] {isDark ? 'text-white/25' : 'text-zinc-400'} transition-colors {isDark ? 'hover:text-white/50' : 'hover:text-zinc-600'}">
		<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
			<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
		</svg>
		Back to payments
	</a>
	<div class="mb-8">
		<p class="mb-1 text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Collections</p>
		<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">
			Send <span class="italic text-emerald-400">Reminders</span>
		</h1>
		{#if overdueInvoices.length > 0}
			<p class="mt-2 text-[13px] {isDark ? 'text-white/30' : 'text-zinc-400'}">{overdueInvoices.length} overdue invoice{overdueInvoices.length !== 1 ? 's' : ''} totalling {formatKES(totalOverdue)}</p>
		{/if}
	</div>

	{#if loading}
		<div class="space-y-4">
			{#each Array(3) as _}
				<div class="animate-pulse rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
					<div class="flex items-center gap-4">
						<div class="h-10 w-10 rounded-lg {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
						<div class="flex-1">
							<div class="h-4 w-40 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
							<div class="mt-2 h-3 w-64 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
						</div>
					</div>
				</div>
			{/each}
		</div>
	{:else if invoices.length === 0}
		<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-12 text-center transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<div class="mx-auto mb-4 flex h-14 w-14 items-center justify-center rounded-full bg-emerald-500/10">
				<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
					<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
				</svg>
			</div>
			<h3 class="mb-2 font-['Instrument_Serif'] text-xl {isDark ? 'text-white' : 'text-zinc-900'}">All caught up!</h3>
			<p class="text-[13px] {isDark ? 'text-white/30' : 'text-zinc-400'}">No outstanding invoices to remind about.</p>
			<a href="/invoices/new" class="mt-6 inline-flex items-center gap-2 rounded-xl bg-emerald-500 px-6 py-2.5 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400">
				Create Invoice
			</a>
		</div>
	{:else}
		<div class="space-y-4 transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			{#if overdueInvoices.length > 0}
				<p class="text-[11px] font-medium uppercase tracking-[0.12em] text-red-400/70">Overdue</p>
			{/if}
			{#each overdueInvoices as inv, i}
				<div class="rounded-2xl border border-red-500/10 bg-red-500/[0.02] p-5 transition-all" style="transition-delay: {i * 40}ms;">
					<div class="flex items-center justify-between gap-4">
						<div class="flex items-center gap-4 min-w-0">
							<img src={getAvatarUrl(inv.client_name)} alt={inv.client_name} class="h-10 w-10 rounded-lg flex-shrink-0" />
							<div class="min-w-0">
								<h3 class="truncate text-[14px] font-semibold {isDark ? 'text-white/80' : 'text-zinc-700'}">{inv.client_name}</h3>
								<p class="mt-0.5 truncate text-[12px] {isDark ? 'text-white/25' : 'text-zinc-400'}">{inv.description}</p>
								<div class="mt-1.5 flex items-center gap-3 text-[11px]">
									<span class="text-red-400 font-medium">{inv.days_overdue}d overdue</span>
									{#if inv.client_email}
										<span class="{isDark ? 'text-white/15' : 'text-zinc-300'}">{inv.client_email}</span>
									{:else}
										<span class="text-amber-400">No email</span>
									{/if}
								</div>
							</div>
						</div>
						<div class="flex items-center gap-4 flex-shrink-0">
							<p class="text-lg font-semibold {isDark ? 'text-white' : 'text-zinc-900'}">{formatKES(inv.amount)}</p>
							<button
								onclick={() => sendReminder(inv)}
								disabled={sendingId === inv.id || !inv.client_email}
								class="rounded-xl bg-emerald-500 px-4 py-2 text-[12px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400 disabled:opacity-40 disabled:cursor-not-allowed"
							>
								{#if sendingId === inv.id}
									<div class="h-3.5 w-3.5 animate-spin rounded-full border-2 border-zinc-950/30 border-t-zinc-950"></div>
								{:else}
									Send Reminder
								{/if}
							</button>
						</div>
					</div>
				</div>
			{/each}

			{#if pendingInvoices.length > 0}
				<p class="mt-6 text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Upcoming / Sent</p>
			{/if}
			{#each pendingInvoices as inv, i}
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-5 transition-all" style="transition-delay: {(overdueInvoices.length + i) * 40}ms;">
					<div class="flex items-center justify-between gap-4">
						<div class="flex items-center gap-4 min-w-0">
							<img src={getAvatarUrl(inv.client_name)} alt={inv.client_name} class="h-10 w-10 rounded-lg flex-shrink-0" />
							<div class="min-w-0">
								<h3 class="truncate text-[14px] font-semibold {isDark ? 'text-white/80' : 'text-zinc-700'}">{inv.client_name}</h3>
								<p class="mt-0.5 truncate text-[12px] {isDark ? 'text-white/25' : 'text-zinc-400'}">{inv.description}</p>
								<div class="mt-1.5 flex items-center gap-3 text-[11px]">
									<span class="{isDark ? 'text-white/20' : 'text-zinc-400'}">Due {new Date(inv.due_date).toLocaleDateString()}</span>
									{#if inv.client_email}
										<span class="{isDark ? 'text-white/15' : 'text-zinc-300'}">{inv.client_email}</span>
									{:else}
										<span class="text-amber-400">No email</span>
									{/if}
								</div>
							</div>
						</div>
						<div class="flex items-center gap-4 flex-shrink-0">
							<p class="text-lg font-semibold {isDark ? 'text-white' : 'text-zinc-900'}">{formatKES(inv.amount)}</p>
							<button
								onclick={() => sendReminder(inv)}
								disabled={sendingId === inv.id || !inv.client_email}
								class="rounded-xl border {isDark ? 'border-white/[0.08]' : 'border-zinc-200'} px-4 py-2 text-[12px] font-medium {isDark ? 'text-white/40' : 'text-zinc-500'} transition-all {isDark ? 'hover:border-white/[0.15] hover:text-white/60' : 'hover:border-zinc-300 hover:text-zinc-700'} disabled:opacity-40 disabled:cursor-not-allowed"
							>
								{#if sendingId === inv.id}
									<div class="h-3.5 w-3.5 animate-spin rounded-full border-2 {isDark ? 'border-white/20 border-t-white/60' : 'border-zinc-300 border-t-zinc-600'}"></div>
								{:else}
									Nudge
								{/if}
							</button>
						</div>
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>
