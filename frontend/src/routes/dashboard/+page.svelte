<script lang="ts">
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { theme } from '$lib/stores/theme';
	import { lastEvent } from '$lib/stores/ws';
	import Icon from '$lib/components/Icon.svelte';

	const isDark = $derived($theme === 'dark');

	interface DashboardData {
		total_receivables: number;
		total_paid: number;
		overdue_count: number;
		total_invoices: number;
	}

	let data = $state<DashboardData | null>(null);
	let loading = $state(true);
	let visible = $state(false);
	let isConfigured = $state(true);

	// AI insights state
	let insights = $state<string | null>(null);
	let insightsLoading = $state(false);
	let insightsError = $state(false);

	onMount(async () => {
		if (!$auth.token) { goto('/login'); return; }
		try {
			const [dashRes, profileRes] = await Promise.all([
				api<DashboardData>('/dashboard/summary'),
				api<{ is_configured: boolean }>('/profile/')
			]);
			data = dashRes;
			isConfigured = profileRes.is_configured;
		} catch {
			data = { total_receivables: 0, total_paid: 0, overdue_count: 0, total_invoices: 0 };
		} finally {
			loading = false;
			setTimeout(() => (visible = true), 50);
		}
		loadInsights();
	});

	// Refresh dashboard data when a payment lands via WebSocket
	$effect(() => {
		if ($lastEvent?.type === 'payment_received' || $lastEvent?.type === 'dashboard_update') {
			api<DashboardData>('/dashboard/summary').then(d => { data = d; loadInsights(); }).catch(() => {});
		}
	});

	async function loadInsights() {
		insightsLoading = true;
		insightsError = false;
		try {
			const res = await api<{ status: string; insights: string }>('/ai/cash-flow-insights', { method: 'POST', token: $auth.token! });
			insights = res.insights;
		} catch {
			insightsError = true;
		} finally {
			insightsLoading = false;
		}
	}

	const recoveryRate = $derived(
		data && data.total_receivables + data.total_paid > 0
			? Math.round((data.total_paid / (data.total_receivables + data.total_paid)) * 100)
			: 0
	);
</script>

<svelte:head>
	<title>Dashboard — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<!-- Header -->
	<div class="mb-8 flex items-end justify-between">
		<div>
			<p class="mb-1 text-[12px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Overview</p>
			<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'} md:text-4xl">
				Welcome back, <span class="italic text-emerald-400">{$auth.name}</span>
			</h1>
		</div>
		<a
			href="/invoices/new"
			class="group hidden items-center gap-2 rounded-xl bg-emerald-500 px-5 py-2.5 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400 sm:inline-flex"
		>
			<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
			</svg>
			New Invoice
		</a>
	</div>

	{#if !loading && !isConfigured}
		<a href="/profile" class="mb-6 flex items-center gap-3 rounded-2xl border border-amber-500/20 bg-amber-500/[0.05] p-4 transition-all hover:bg-amber-500/[0.08]">
			<div class="flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-lg bg-amber-500/10">
				<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
				</svg>
			</div>
			<div class="flex-1">
				<p class="text-[13px] font-medium text-amber-400">Complete your business profile</p>
				<p class="text-[11px] {isDark ? 'text-white/30' : 'text-zinc-500'}">Add your logo and address to enable branded invoices and shareable payment links</p>
			</div>
			<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-amber-400/50" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M8.25 4.5l7.5 7.5-7.5 7.5" />
			</svg>
		</a>
	{/if}

	{#if loading}
		<div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
			{#each Array(4) as _}
				<div class="animate-pulse rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
					<div class="mb-3 h-3 w-20 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-200'}"></div>
					<div class="h-8 w-28 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-200'}"></div>
				</div>
			{/each}
		</div>
	{:else if data}
		<!-- Stats Grid -->
		<div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
			<div class="rounded-2xl border border-emerald-500/10 bg-emerald-500/[0.03] p-6 transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-4 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] text-emerald-500/70">Expected</span>
					<div class="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500/10">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z" />
						</svg>
					</div>
				</div>
				<p class="text-2xl font-bold tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">{formatKES(data.total_receivables)}</p>
				<div class="mt-3 flex items-center gap-2">
					<div class="h-1 flex-1 rounded-full {isDark ? 'bg-white/[0.04]' : 'bg-zinc-200'}">
						<div class="h-full rounded-full bg-emerald-500/50 transition-all duration-1000" style="width: {recoveryRate}%"></div>
					</div>
					<span class="text-[11px] {isDark ? 'text-white/25' : 'text-zinc-400'}">{recoveryRate}%</span>
				</div>
			</div>

			<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 transition-all duration-500 delay-75 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-4 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Collected</span>
					<div class="flex h-8 w-8 items-center justify-center rounded-lg {isDark ? 'bg-white/[0.03]' : 'bg-zinc-100'}">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {isDark ? 'text-white/30' : 'text-zinc-400'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.745 3.745 0 011.043 3.296A3.745 3.745 0 0121 12z" />
						</svg>
					</div>
				</div>
				<p class="text-2xl font-bold tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">{formatKES(data.total_paid)}</p>
				<p class="mt-2 text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">via M-Pesa</p>
			</div>

			<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 transition-all duration-500 delay-150 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-4 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Invoices</span>
					<div class="flex h-8 w-8 items-center justify-center rounded-lg {isDark ? 'bg-white/[0.03]' : 'bg-zinc-100'}">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {isDark ? 'text-white/30' : 'text-zinc-400'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
						</svg>
					</div>
				</div>
				<p class="text-2xl font-bold tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">{data.total_invoices}</p>
				<p class="mt-2 text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">total created</p>
			</div>

			<div class="rounded-2xl border p-6 transition-all duration-500 delay-200 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'} {data.overdue_count > 0 ? 'border-amber-500/10 bg-amber-500/[0.03]' : isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'}">
				<div class="mb-4 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] {data.overdue_count > 0 ? 'text-amber-500/70' : isDark ? 'text-white/25' : 'text-zinc-400'}">Overdue</span>
					<div class="flex h-8 w-8 items-center justify-center rounded-lg {data.overdue_count > 0 ? 'bg-amber-500/10' : isDark ? 'bg-white/[0.03]' : 'bg-zinc-100'}">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {data.overdue_count > 0 ? 'text-amber-400' : isDark ? 'text-white/30' : 'text-zinc-400'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
						</svg>
					</div>
				</div>
				<p class="text-2xl font-bold tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">{data.overdue_count}</p>
				<p class="mt-2 text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">past due date</p>
			</div>
		</div>

		<!-- Bottom Row -->
		<div class="mt-4 grid grid-cols-1 gap-4 lg:grid-cols-12">
			<!-- Collection Overview -->
			<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 lg:col-span-5 transition-all duration-500 delay-300 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-6 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Collection Overview</span>
					<span class="text-[11px] {isDark ? 'text-white/15' : 'text-zinc-300'}">All time</span>
				</div>
				<div class="flex items-end gap-8">
					<div>
						<p class="font-['Instrument_Serif'] text-5xl italic tracking-tight text-emerald-400 md:text-6xl">{recoveryRate}%</p>
						<p class="mt-1 text-[12px] {isDark ? 'text-white/25' : 'text-zinc-400'}">Recovery Rate</p>
					</div>
					<div class="flex flex-1 items-end gap-2 pb-1">
						{#each [
							{ label: 'Total', value: data.total_invoices, color: isDark ? 'bg-white/[0.06]' : 'bg-zinc-200' },
							{ label: 'Paid', value: data.total_paid > 0 ? Math.round((data.total_paid / Math.max(data.total_receivables + data.total_paid, 1)) * data.total_invoices) : 0, color: 'bg-emerald-500/40' },
							{ label: 'Overdue', value: data.overdue_count, color: 'bg-amber-500/40' }
						] as bar}
							<div class="flex flex-1 flex-col items-center gap-2">
								<div class="w-full rounded-lg {bar.color} transition-all duration-1000" style="height: {Math.max((bar.value / Math.max(data.total_invoices, 1)) * 100, 6)}px"></div>
								<span class="text-[10px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{bar.label}</span>
							</div>
						{/each}
					</div>
				</div>
			</div>

			<!-- AI Insights -->
			<div class="rounded-2xl border border-violet-500/10 bg-violet-500/[0.02] p-6 lg:col-span-7 transition-all duration-500 delay-350 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-4 flex items-center justify-between">
					<div class="flex items-center gap-2.5">
						<div class="flex h-7 w-7 items-center justify-center rounded-lg bg-violet-500/10">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
							</svg>
						</div>
						<span class="text-[11px] font-medium uppercase tracking-[0.12em] text-violet-400/70">AI Insights</span>
					</div>
					<button
						onclick={loadInsights}
						disabled={insightsLoading}
						class="flex items-center gap-1.5 rounded-lg px-2.5 py-1 text-[11px] {isDark ? 'text-white/20 hover:text-white/40' : 'text-zinc-400 hover:text-zinc-600'} transition-colors disabled:opacity-40"
					>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 {insightsLoading ? 'animate-spin' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
						</svg>
						Refresh
					</button>
				</div>

				{#if insightsLoading}
					<div class="space-y-2.5">
						{#each Array(3) as _}
							<div class="animate-pulse">
								<div class="h-3 w-full rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
								<div class="mt-1.5 h-3 w-4/5 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
							</div>
						{/each}
					</div>
				{:else if insightsError}
					<p class="text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Could not load insights. <button onclick={loadInsights} class="text-violet-400 hover:text-violet-300">Try again</button></p>
				{:else if insights}
					<div class="space-y-3">
						{#each insights.split('\n').filter(l => l.trim()) as line}
							<p class="text-[13px] leading-relaxed {isDark ? 'text-white/50' : 'text-zinc-600'}">{line}</p>
						{/each}
					</div>
				{:else}
					<p class="text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'}">No data yet — create some invoices to get AI insights.</p>
				{/if}
			</div>
		</div>

		<!-- Quick Actions row -->
		<div class="mt-4 rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 transition-all duration-500 delay-400 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Quick Actions</span>
			<div class="grid grid-cols-2 gap-2 md:grid-cols-4">
				{#each [
					{ href: '/invoices/new',     label: 'New Invoice',     sub: 'AI or manual',               icon: 'record-payment',  accent: true },
					{ href: '/payments/request', label: 'Request Payment', sub: 'Send M-Pesa push',           icon: 'request-payment', accent: false },
					{ href: '/payments/remind',  label: 'Send Reminder',   sub: 'Nudge late clients',         icon: 'send-reminder',   accent: false },
					{ href: '/reports',          label: 'View Reports',    sub: 'Cash flow breakdown',        icon: 'create-group',    accent: false }
				] as action}
					<a
						href={action.href}
						class="group flex items-center gap-3 rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} p-3 transition-all {isDark ? 'hover:border-white/[0.08]' : 'hover:border-zinc-300'} {isDark ? 'hover:bg-white/[0.02]' : 'hover:bg-zinc-50'}"
					>
						<div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg {action.accent ? 'bg-emerald-500/10' : isDark ? 'bg-white/[0.03]' : 'bg-zinc-100'}">
							<Icon name={action.icon} stroke={action.accent ? 'rgba(52,211,153,1)' : isDark ? 'rgba(255,255,255,0.3)' : 'rgba(113,113,122,1)'} />
						</div>
						<div>
							<p class="text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">{action.label}</p>
							<p class="text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{action.sub}</p>
						</div>
					</a>
				{/each}
			</div>
		</div>
	{/if}
</div>
