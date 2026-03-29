<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { theme } from '$lib/stores/theme';
	import { getAvatarUrl } from '$lib/avatar';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	const isDark = $derived($theme === 'dark');

	interface ImarishaData {
		expected_inflow: number;
		money_in_motion: number;
		collected: number;
		at_risk: number;
	}

	let data = $state<ImarishaData | null>(null);
	let loading = $state(true);
	let visible = $state(false);

	interface Contribution {
		id: number;
		member: string;
		amount: number;
		status: string;
		timestamp: string;
		rule: string;
	}

	let contributions = $state<Contribution[]>([]);

	onMount(async () => {
		if (!$auth.token) { goto('/imarisha'); return; }
		try {
			// TODO: Wire to Imarisha backend when available
			data = { expected_inflow: 0, money_in_motion: 0, collected: 0, at_risk: 0 };
		} catch {
			data = { expected_inflow: 0, money_in_motion: 0, collected: 0, at_risk: 0 };
		} finally {
			loading = false;
			setTimeout(() => (visible = true), 50);
		}
	});

	function getStatusColor(status: string) {
		switch (status) {
			case 'completed': return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
			case 'pending': return 'bg-amber-500/10 text-amber-400 border-amber-500/20';
			case 'failed': return 'bg-red-500/10 text-red-400 border-red-500/20';
			default: return isDark ? 'bg-white/[0.05] text-white/60 border-white/[0.10]' : 'bg-zinc-100 text-zinc-600 border-zinc-200';
		}
	}

	function getStatusText(status: string) {
		switch (status) {
			case 'completed': return 'Completed';
			case 'pending': return 'Pending';
			case 'failed': return 'Failed';
			default: return 'Unknown';
		}
	}
</script>

<svelte:head>
	<title>Imarisha Dashboard — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<!-- Header -->
	<div class="mb-8 flex items-end justify-between">
		<div>
			<p class="mb-1 text-[12px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Chama Dashboard</p>
			<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'} md:text-4xl">
				Welcome back, <span class="italic text-emerald-400">{$auth.name}</span>
			</h1>
		</div>
		<a
			href="/groups/create"
			class="group hidden items-center gap-2 rounded-xl bg-emerald-500 px-5 py-2.5 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400 sm:inline-flex"
		>
			<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
			</svg>
			Manage Group
		</a>
	</div>

	{#if loading}
		<!-- Skeleton -->
		<div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
			{#each Array(4) as _}
				<div class="animate-pulse rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
					<div class="mb-3 h-3 w-20 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-200'}"></div>
					<div class="h-8 w-28 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-200'}"></div>
				</div>
			{/each}
		</div>
	{:else if data}
		<!-- Top Summary Cards -->
		<div class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
			<!-- Expected Inflow -->
			<div class="rounded-2xl border border-emerald-500/10 bg-emerald-500/[0.03] p-6 transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-4 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] text-emerald-500/70">Expected Inflow</span>
					<div class="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500/10">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" />
						</svg>
					</div>
				</div>
				<p class="text-2xl font-bold tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">{formatKES(data.expected_inflow)}</p>
				<p class="mt-2 text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">scheduled for automatic deduction</p>
			</div>

			<!-- Money in Motion -->
			<div class="rounded-2xl border border-amber-500/10 bg-amber-500/[0.03] p-6 transition-all duration-500 delay-75 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-4 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] text-amber-500/70">Money in Motion</span>
					<div class="flex h-8 w-8 items-center justify-center rounded-lg bg-amber-500/10">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m6-6H6" />
						</svg>
					</div>
				</div>
				<p class="text-2xl font-bold tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">{formatKES(data.money_in_motion)}</p>
				<p class="mt-2 text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">pending STK pushes</p>
			</div>

			<!-- Collected -->
			<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 transition-all duration-500 delay-150 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-4 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Collected</span>
					<div class="flex h-8 w-8 items-center justify-center rounded-lg {isDark ? 'bg-white/[0.03]' : 'bg-white'}">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {isDark ? 'text-white/30' : 'text-zinc-400'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.745 3.745 0 011.043 3.296A3.745 3.745 0 0121 12z" />
						</svg>
					</div>
				</div>
				<p class="text-2xl font-bold tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">{formatKES(data.collected)}</p>
				<p class="mt-2 text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">completed contributions</p>
			</div>

			<!-- At Risk -->
			<div class="rounded-2xl border border-red-500/10 bg-red-500/[0.03] p-6 transition-all duration-500 delay-200 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-4 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] text-red-500/70">At Risk</span>
					<div class="flex h-8 w-8 items-center justify-center rounded-lg bg-red-500/10">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z" />
						</svg>
					</div>
				</div>
				<p class="text-2xl font-bold tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">{formatKES(data.at_risk)}</p>
				<p class="mt-2 text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">failed or delayed transactions</p>
			</div>
		</div>

		<!-- Bottom Row -->
		<div class="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-12">
			<!-- Contributions Feed -->
			<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 lg:col-span-8 transition-all duration-500 delay-300 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-6 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Contributions Feed</span>
					<div class="flex items-center gap-2">
						<span class="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
						<span class="text-[10px] {isDark ? 'text-white/40' : 'text-zinc-500'}">Live</span>
					</div>
				</div>

				{#if contributions.length === 0}
					<div class="text-center py-12">
						<div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full {isDark ? 'bg-white/[0.05]' : 'bg-zinc-100'}">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 {isDark ? 'text-white/30' : 'text-zinc-400'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
							</svg>
						</div>
						<p class="text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'}">No contributions yet</p>
						<p class="mt-1 text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Create a group and add members to start collecting</p>
					</div>
				{:else}
					<div class="space-y-3">
						{#each contributions as contribution}
							<div class="rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.01]' : 'bg-white'} p-4 transition-all {isDark ? 'hover:border-white/[0.08]' : 'hover:border-zinc-300'}">
								<div class="flex items-center justify-between">
									<div class="flex items-center gap-3">
										<img src={getAvatarUrl(contribution.member)} alt={contribution.member} class="h-10 w-10 rounded-full" />
										<div>
											<p class="text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">{contribution.member}</p>
											<p class="text-[11px] {isDark ? 'text-white/40' : 'text-zinc-500'}">{contribution.rule} • {contribution.timestamp}</p>
										</div>
									</div>
									<div class="text-right">
										<p class="text-lg font-medium {isDark ? 'text-white' : 'text-zinc-900'}">{formatKES(contribution.amount)}</p>
										<span class="inline-block mt-1 rounded-full px-2 py-0.5 text-[10px] font-medium {getStatusColor(contribution.status)}">
											{getStatusText(contribution.status)}
										</span>
									</div>
								</div>
							</div>
						{/each}
					</div>
				{/if}
			</div>

			<!-- Quick Actions & AI Indicator -->
			<div class="space-y-6 lg:col-span-4">
				<!-- Quick Actions -->
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 transition-all duration-500 delay-400 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Quick Actions</span>
					<div class="space-y-2">
						<a href="/imarisha/contributions" class="flex items-center gap-3 rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} p-3 transition-all {isDark ? 'hover:border-white/[0.08]' : 'hover:border-zinc-300'} {isDark ? 'hover:bg-white/[0.02]' : 'hover:bg-zinc-50'}">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {isDark ? 'text-white/30' : 'text-zinc-400'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
							</svg>
							<div>
								<p class="text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">View Contribution Details</p>
								<p class="text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Full audit trail</p>
							</div>
						</a>
						<button class="flex items-center gap-3 rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} p-3 transition-all {isDark ? 'hover:border-white/[0.08]' : 'hover:border-zinc-300'} {isDark ? 'hover:bg-white/[0.02]' : 'hover:bg-zinc-50'}">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {isDark ? 'text-white/30' : 'text-zinc-400'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75c-.778 0-1.504.357-1.96.966l-.314.378a8.967 8.967 0 01-1.96-.966 8.967 8.967 0 00-1.96.966l-.314-.378A2.464 2.464 0 019.75 9.75a8.967 8.967 0 00-1.311 5.454M12 20.25a8.967 8.967 0 01-5.454-1.31m10.91 0a23.848 23.848 0 005.454-1.31" />
							</svg>
							<div>
								<p class="text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Send Reminder</p>
								<p class="text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">For failed deductions</p>
							</div>
						</button>
						<button class="flex items-center gap-3 rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} p-3 transition-all {isDark ? 'hover:border-white/[0.08]' : 'hover:border-zinc-300'} {isDark ? 'hover:bg-white/[0.02]' : 'hover:bg-zinc-50'}">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {isDark ? 'text-white/30' : 'text-zinc-400'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197A5.971 5.971 0 006 18.72v-2.007m0 0V18.72v-2.007m0 0a5.971 5.971 0 00-.941 3.197M5.058 15.522A5.971 5.971 0 006 18.72v-2.007M5.058 15.522A5.971 5.971 0 016 12.75v2.007m0 0A5.971 5.971 0 00.941 3.197m8.018-8.018a5.971 5.971 0 00-.941-3.197M6 12.75a5.971 5.971 0 01.941-3.197m5.059 5.059a5.971 5.971 0 01-.941 3.197M12 12.75a5.971 5.971 0 01-.941-3.197m0 6.394a5.971 5.971 0 00.941-3.197m0-6.394a5.971 5.971 0 00-.941 3.197" />
							</svg>
							<div>
								<p class="text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Add Member / Edit Rules</p>
								<p class="text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Manage group settings</p>
							</div>
						</button>
					</div>
				</div>

				<!-- AI / Automation Indicator -->
				<div class="rounded-2xl border border-emerald-500/10 bg-emerald-500/[0.03] p-6 transition-all duration-500 delay-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<div class="mb-4 flex items-center gap-2">
						<div class="flex h-6 w-6 items-center justify-center rounded-full bg-emerald-400">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
							</svg>
						</div>
						<span class="text-[11px] font-medium text-emerald-400">AI Automation Active</span>
					</div>
					<p class="text-[12px] {isDark ? 'text-white/60' : 'text-zinc-600'}">Contributions will be automatically processed and tracked once your group is set up.</p>
					<div class="mt-3">
						<div class="mb-2 flex items-center justify-between text-[10px] {isDark ? 'text-white/40' : 'text-zinc-500'}">
							<span>Automation Status</span>
							<span class="text-emerald-400">{contributions.length > 0 ? 'Active' : 'Ready'}</span>
						</div>
						<div class="h-2 w-full rounded-full {isDark ? 'bg-white/[0.04]' : 'bg-zinc-200'}">
							<div class="h-full rounded-full bg-emerald-500/50 transition-all duration-1000" style="width: {contributions.length > 0 ? '100' : '0'}%"></div>
						</div>
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>
