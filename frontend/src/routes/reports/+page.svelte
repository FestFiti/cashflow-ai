<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { theme } from '$lib/stores/theme';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { api, formatKES } from '$lib/api';
	import { getAvatarUrl } from '$lib/avatar';

	const isDark = $derived($theme === 'dark');
	let visible = $state(false);
	let loading = $state(true);

	interface Overview {
		total_invoiced: number;
		total_collected: number;
		total_outstanding: number;
		overdue_amount: number;
		invoice_count: number;
		paid_count: number;
		overdue_count: number;
		collection_rate: number;
		invoiced_30d: number;
		collected_30d: number;
	}
	interface RevenueMonth { month: string; invoiced: number; collected: number; }
	interface StatusItem { status: string; count: number; amount: number; }
	interface TopClient { client_name: string; invoice_count: number; total_amount: number; paid_amount: number; collection_rate: number; }
	interface AgingBucket { label: string; count: number; amount: number; }
	interface RecentPayment { id: string; client_name: string; amount: number; mpesa_receipt: string | null; paid_at: string | null; }

	let overview = $state<Overview | null>(null);
	let revenueChart = $state<RevenueMonth[]>([]);
	let statusBreakdown = $state<StatusItem[]>([]);
	let topClients = $state<TopClient[]>([]);
	let aging = $state<AgingBucket[]>([]);
	let recentPayments = $state<RecentPayment[]>([]);

	const maxRevenue = $derived(Math.max(...revenueChart.map(m => Math.max(m.invoiced, m.collected)), 1));

	async function downloadCSV(path: string, filename: string) {
		const res = await fetch(`/api${path}`, {
			headers: { Authorization: `Bearer ${$auth.token}` }
		});
		if (!res.ok) return;
		const blob = await res.blob();
		const url = URL.createObjectURL(blob);
		const a = document.createElement('a');
		a.href = url;
		a.download = filename;
		a.click();
		URL.revokeObjectURL(url);
	}

	const statusColors: Record<string, string> = {
		paid: 'bg-emerald-500',
		sent: 'bg-blue-500',
		overdue: 'bg-amber-500',
		draft: 'bg-zinc-500',
	};
	const statusTextColors: Record<string, string> = {
		paid: 'text-emerald-400',
		sent: 'text-blue-400',
		overdue: 'text-amber-400',
		draft: isDark ? 'text-white/40' : 'text-zinc-500',
	};

	onMount(async () => {
		if (!$auth.token) { goto('/login'); return; }
		try {
			const [ov, rc, sb, tc, ag, rp] = await Promise.all([
				api<Overview>('/reports/overview', { token: $auth.token }),
				api<RevenueMonth[]>('/reports/revenue-chart?months=6', { token: $auth.token }),
				api<StatusItem[]>('/reports/status-breakdown', { token: $auth.token }),
				api<TopClient[]>('/reports/top-clients?limit=5', { token: $auth.token }),
				api<AgingBucket[]>('/reports/aging', { token: $auth.token }),
				api<RecentPayment[]>('/reports/recent-payments?limit=8', { token: $auth.token }),
			]);
			overview = ov;
			revenueChart = rc;
			statusBreakdown = sb;
			topClients = tc;
			aging = ag;
			recentPayments = rp;
		} catch {
			// fallback — API may not be ready
		} finally {
			loading = false;
			setTimeout(() => (visible = true), 50);
		}
	});
</script>

<svelte:head>
	<title>Reports — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<!-- Header -->
	<div class="mb-8 flex items-end justify-between">
		<div>
			<p class="mb-1 text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Analytics</p>
			<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'} md:text-4xl">
				<span class="italic text-emerald-400">Reports</span>
			</h1>
		</div>
		{#if overview}
			<div class="flex gap-2">
				<button
					onclick={() => downloadCSV('/reports/export/invoices', 'invoices.csv')}
					class="inline-flex items-center gap-1.5 rounded-xl border px-4 py-2 text-[12px] font-medium transition-all {isDark ? 'border-white/[0.08] text-white/50 hover:border-white/20 hover:text-white' : 'border-zinc-200 text-zinc-500 hover:border-zinc-300 hover:text-zinc-700'}"
				>
					<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3"/></svg>
					Invoices
				</button>
				<button
					onclick={() => downloadCSV('/reports/export/payments', 'payments.csv')}
					class="inline-flex items-center gap-1.5 rounded-xl border px-4 py-2 text-[12px] font-medium transition-all {isDark ? 'border-white/[0.08] text-white/50 hover:border-white/20 hover:text-white' : 'border-zinc-200 text-zinc-500 hover:border-zinc-300 hover:text-zinc-700'}"
				>
					<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3"/></svg>
					Payments
				</button>
				<button
					onclick={() => downloadCSV('/reports/export/clients', 'clients.csv')}
					class="inline-flex items-center gap-1.5 rounded-xl border px-4 py-2 text-[12px] font-medium transition-all {isDark ? 'border-white/[0.08] text-white/50 hover:border-white/20 hover:text-white' : 'border-zinc-200 text-zinc-500 hover:border-zinc-300 hover:text-zinc-700'}"
				>
					<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3"/></svg>
					Clients
				</button>
			</div>
		{/if}
	</div>

	{#if loading}
		<div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
			{#each Array(4) as _}
				<div class="animate-pulse rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
					<div class="h-3 w-20 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
					<div class="mt-3 h-8 w-32 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
				</div>
			{/each}
		</div>
	{:else if overview}
		<!-- KPI Cards -->
		<div class="grid gap-4 md:grid-cols-2 lg:grid-cols-4 transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
				<div class="flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Total Invoiced</span>
					<div class="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500/10">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m-3-2.818l.879.659c1.171.879 3.07.879 4.242 0 1.172-.879 1.172-2.303 0-3.182C13.536 12.219 12.768 12 12 12c-.725 0-1.45-.22-2.003-.659-1.106-.879-1.106-2.303 0-3.182s2.9-.879 4.006 0l.415.33M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
					</div>
				</div>
				<p class="mt-3 font-['Instrument_Serif'] text-3xl italic tracking-tight text-emerald-400">{formatKES(overview.total_invoiced)}</p>
				<p class="mt-1 text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{overview.invoice_count} invoices</p>
			</div>
			<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
				<div class="flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Collected</span>
					<div class="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-500/10">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.745 3.745 0 011.043 3.296A3.745 3.745 0 0121 12z" /></svg>
					</div>
				</div>
				<p class="mt-3 font-['Instrument_Serif'] text-3xl italic tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">{formatKES(overview.total_collected)}</p>
				<p class="mt-1 text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{overview.paid_count} paid · {overview.collection_rate}% rate</p>
			</div>
			<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
				<div class="flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Outstanding</span>
					<div class="flex h-8 w-8 items-center justify-center rounded-lg bg-amber-500/10">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
					</div>
				</div>
				<p class="mt-3 font-['Instrument_Serif'] text-3xl italic tracking-tight text-amber-400">{formatKES(overview.total_outstanding)}</p>
				<p class="mt-1 text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">awaiting payment</p>
			</div>
			<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
				<div class="flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Overdue</span>
					<div class="flex h-8 w-8 items-center justify-center rounded-lg bg-red-500/10">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" /></svg>
					</div>
				</div>
				<p class="mt-3 font-['Instrument_Serif'] text-3xl italic tracking-tight text-red-400">{formatKES(overview.overdue_amount)}</p>
				<p class="mt-1 text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{overview.overdue_count} overdue</p>
			</div>
		</div>

		<!-- 30-Day Snapshot -->
		<div class="mt-4 grid gap-4 md:grid-cols-2 transition-all duration-500 delay-100 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
				<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Invoiced (Last 30 Days)</span>
				<p class="mt-2 font-['Instrument_Serif'] text-2xl italic tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">{formatKES(overview.invoiced_30d)}</p>
			</div>
			<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
				<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Collected (Last 30 Days)</span>
				<p class="mt-2 font-['Instrument_Serif'] text-2xl italic tracking-tight text-emerald-400">{formatKES(overview.collected_30d)}</p>
			</div>
		</div>

		<div class="mt-4 grid gap-4 lg:grid-cols-12 transition-all duration-500 delay-200 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<!-- Revenue Chart -->
			<div class="lg:col-span-8 rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
				<div class="mb-6 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Revenue (6 Months)</span>
					<div class="flex items-center gap-4">
						<div class="flex items-center gap-1.5"><div class="h-2 w-2 rounded-full bg-emerald-500"></div><span class="text-[11px] {isDark ? 'text-white/30' : 'text-zinc-400'}">Invoiced</span></div>
						<div class="flex items-center gap-1.5"><div class="h-2 w-2 rounded-full bg-blue-500"></div><span class="text-[11px] {isDark ? 'text-white/30' : 'text-zinc-400'}">Collected</span></div>
					</div>
				</div>
				{#if revenueChart.length > 0}
					<div class="flex items-end gap-3" style="height: 200px;">
						{#each revenueChart as month}
							<div class="flex flex-1 flex-col items-center gap-1">
								<div class="flex w-full items-end justify-center gap-1" style="height: 170px;">
									<div
										class="w-5 rounded-t bg-emerald-500/70 transition-all duration-700"
										style="height: {maxRevenue > 0 ? (month.invoiced / maxRevenue) * 100 : 0}%"
									></div>
									<div
										class="w-5 rounded-t bg-blue-500/70 transition-all duration-700"
										style="height: {maxRevenue > 0 ? (month.collected / maxRevenue) * 100 : 0}%"
									></div>
								</div>
								<span class="text-[10px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{month.month.split(' ')[0]}</span>
							</div>
						{/each}
					</div>
				{:else}
					<div class="flex h-[200px] items-center justify-center">
						<p class="text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'}">No data yet</p>
					</div>
				{/if}
			</div>

			<!-- Status Breakdown -->
			<div class="lg:col-span-4 rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
				<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Invoice Status</span>
				{#if statusBreakdown.length > 0}
					<div class="space-y-3">
						{#each statusBreakdown as item}
							{@const total = statusBreakdown.reduce((s, i) => s + i.count, 0)}
							{@const pct = total > 0 ? Math.round((item.count / total) * 100) : 0}
							<div>
								<div class="mb-1 flex items-center justify-between">
									<span class="text-[13px] font-medium capitalize {isDark ? 'text-white/60' : 'text-zinc-600'}">{item.status}</span>
									<span class="text-[12px] {isDark ? 'text-white/30' : 'text-zinc-400'}">{item.count} · {formatKES(item.amount)}</span>
								</div>
								<div class="h-1.5 w-full rounded-full {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}">
									<div class="h-full rounded-full {statusColors[item.status] || 'bg-zinc-400'} transition-all duration-700" style="width: {pct}%"></div>
								</div>
							</div>
						{/each}
					</div>
				{:else}
					<p class="text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'}">No invoices yet</p>
				{/if}
			</div>
		</div>

		<div class="mt-4 grid gap-4 lg:grid-cols-12 transition-all duration-500 delay-300 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<!-- Top Clients -->
			<div class="lg:col-span-7 rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
				<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Top Clients</span>
				{#if topClients.length > 0}
					<div class="space-y-3">
						{#each topClients as client, i}
							<div class="flex items-center gap-3 rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-100'} p-3">
								<img src={getAvatarUrl(client.client_name)} alt={client.client_name} class="h-9 w-9 rounded-lg" />
								<div class="min-w-0 flex-1">
									<div class="flex items-center justify-between">
										<p class="truncate text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">{client.client_name}</p>
										<p class="text-[13px] font-semibold text-emerald-400">{formatKES(client.total_amount)}</p>
									</div>
									<div class="mt-1 flex items-center justify-between">
										<p class="text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{client.invoice_count} invoices</p>
										<p class="text-[11px] {client.collection_rate >= 80 ? 'text-emerald-400' : client.collection_rate >= 50 ? 'text-amber-400' : 'text-red-400'}">{client.collection_rate}% collected</p>
									</div>
								</div>
							</div>
						{/each}
					</div>
				{:else}
					<p class="text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'}">No client data yet</p>
				{/if}
			</div>

			<!-- Aging Report -->
			<div class="lg:col-span-5 rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
				<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Receivables Aging</span>
				{#if aging.length > 0}
					<div class="space-y-2">
						{#each aging as bucket, i}
							{@const colors = ['bg-emerald-500', 'bg-blue-500', 'bg-amber-500', 'bg-orange-500', 'bg-red-500']}
							<div class="flex items-center gap-3 rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-100'} p-3">
								<div class="h-2 w-2 rounded-full {colors[i] || 'bg-zinc-400'}"></div>
								<div class="flex-1">
									<p class="text-[13px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">{bucket.label}</p>
								</div>
								<div class="text-right">
									<p class="text-[13px] font-semibold {isDark ? 'text-white/80' : 'text-zinc-700'}">{formatKES(bucket.amount)}</p>
									<p class="text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{bucket.count} invoice{bucket.count !== 1 ? 's' : ''}</p>
								</div>
							</div>
						{/each}
					</div>
				{:else}
					<p class="text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'}">No outstanding invoices</p>
				{/if}
			</div>
		</div>

		<!-- Recent Payments -->
		<div class="mt-4 rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 transition-all duration-500 delay-400 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Recent Payments</span>
			{#if recentPayments.length > 0}
				<div class="overflow-x-auto">
					<table class="w-full">
						<thead>
							<tr class="border-b {isDark ? 'border-white/[0.04]' : 'border-zinc-100'}">
								<th class="pb-3 text-left text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Client</th>
								<th class="pb-3 text-left text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Amount</th>
								<th class="pb-3 text-left text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Receipt</th>
								<th class="pb-3 text-right text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Date</th>
							</tr>
						</thead>
						<tbody>
							{#each recentPayments as payment}
								<tr class="border-b {isDark ? 'border-white/[0.02]' : 'border-zinc-50'}">
									<td class="py-3">
										<div class="flex items-center gap-2.5">
											<img src={getAvatarUrl(payment.client_name)} alt={payment.client_name} class="h-7 w-7 rounded-md" />
											<span class="text-[13px] font-medium {isDark ? 'text-white/70' : 'text-zinc-700'}">{payment.client_name}</span>
										</div>
									</td>
									<td class="py-3 text-[13px] font-semibold text-emerald-400">{formatKES(payment.amount)}</td>
									<td class="py-3 text-[12px] font-mono {isDark ? 'text-white/30' : 'text-zinc-400'}">{payment.mpesa_receipt || '—'}</td>
									<td class="py-3 text-right text-[12px] {isDark ? 'text-white/30' : 'text-zinc-400'}">{payment.paid_at ? new Date(payment.paid_at).toLocaleDateString() : '—'}</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{:else}
				<p class="text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'}">No payments received yet</p>
			{/if}
		</div>
	{:else}
		<!-- Fallback empty state -->
		<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-12 text-center transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<div class="mx-auto flex h-14 w-14 items-center justify-center rounded-lg bg-emerald-500/10">
				<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
					<path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
				</svg>
			</div>
			<h3 class="mt-5 font-['Instrument_Serif'] text-xl {isDark ? 'text-white' : 'text-zinc-900'}">No data to report</h3>
			<p class="mx-auto mt-2 max-w-sm text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Create some invoices and collect payments to see your reports here.</p>
		</div>
	{/if}
</div>
