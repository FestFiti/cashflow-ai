<script lang="ts">
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';

	interface DashboardData {
		total_receivables: number;
		total_paid: number;
		overdue_count: number;
		total_invoices: number;
	}

	let data = $state<DashboardData | null>(null);
	let loading = $state(true);

	onMount(async () => {
		if (!$auth.token) {
			goto('/login');
			return;
		}
		try {
			data = await api<DashboardData>('/dashboard/summary', { token: $auth.token });
		} catch {
			// API not available yet - show demo data
			data = { total_receivables: 0, total_paid: 0, overdue_count: 0, total_invoices: 0 };
		} finally {
			loading = false;
		}
	});

	const recoveryRate = $derived(
		data && data.total_receivables + data.total_paid > 0
			? Math.round((data.total_paid / (data.total_receivables + data.total_paid)) * 100)
			: 0
	);
</script>

<svelte:head>
	<title>Dashboard — CashFlow AI</title>
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8">
	<div class="mb-8 flex items-center justify-between">
		<div>
			<h1 class="text-2xl font-bold tracking-tight md:text-3xl">Dashboard</h1>
			<p class="mt-1 text-sm text-zinc-500">Welcome back, {$auth.name}</p>
		</div>
		<a
			href="/invoices/new"
			class="gradient-bg-emerald inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-5 py-2.5 text-sm font-semibold text-white transition-all hover:bg-emerald-500"
		>
			<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
				<path fill-rule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clip-rule="evenodd" />
			</svg>
			New Invoice
		</a>
	</div>

	{#if loading}
		<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
			{#each Array(4) as _}
				<div class="animate-pulse rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-6">
					<div class="mb-3 h-3 w-24 rounded bg-zinc-800"></div>
					<div class="h-8 w-32 rounded bg-zinc-800"></div>
				</div>
			{/each}
		</div>
	{:else if data}
		<!-- Stats Grid -->
		<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-12">
			<!-- Receivables Card -->
			<div
				class="gradient-bg-emerald animate-fade-in-up rounded-[20px] border border-emerald-500/20 bg-emerald-500/5 p-6 lg:col-span-4"
			>
				<div class="mb-1 flex items-center gap-2">
					<div class="h-2.5 w-2.5 rounded-full bg-emerald-400"></div>
					<span class="text-xs font-medium uppercase tracking-widest text-emerald-500">Receivables</span>
				</div>
				<p class="mt-3 text-3xl font-black tracking-tight">{formatKES(data.total_receivables)}</p>
				<p class="mt-1 text-sm text-zinc-500">{data.total_invoices} total invoices</p>
				<div class="mt-4 h-1.5 overflow-hidden rounded-full bg-zinc-800">
					<div
						class="h-full rounded-full bg-emerald-500 transition-all duration-1000"
						style="width: {recoveryRate}%"
					></div>
				</div>
				<p class="mt-2 text-xs text-zinc-500">{recoveryRate}% collected</p>
			</div>

			<!-- Paid Card -->
			<div
				class="gradient-bg animate-fade-in-up animation-delay-100 rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-6 lg:col-span-4"
			>
				<div class="mb-1 flex items-center gap-2">
					<div class="h-2.5 w-2.5 rounded-full bg-blue-400"></div>
					<span class="text-xs font-medium uppercase tracking-widest text-zinc-500">Total Collected</span>
				</div>
				<p class="mt-3 text-3xl font-black tracking-tight">{formatKES(data.total_paid)}</p>
				<p class="mt-1 text-sm text-zinc-500">via M-Pesa</p>
			</div>

			<!-- Overdue Card -->
			<div
				class="animate-fade-in-up animation-delay-200 rounded-[20px] border p-6 lg:col-span-4"
				class:border-amber-500/20={data.overdue_count > 0}
				class:bg-amber-500/5={data.overdue_count > 0}
				class:gradient-bg-amber={data.overdue_count > 0}
				class:border-zinc-800={data.overdue_count === 0}
				class:bg-zinc-900/30={data.overdue_count === 0}
				class:gradient-bg={data.overdue_count === 0}
			>
				<div class="mb-1 flex items-center gap-2">
					<div class="h-2.5 w-2.5 rounded-full" class:bg-amber-400={data.overdue_count > 0} class:bg-zinc-500={data.overdue_count === 0}></div>
					<span class="text-xs font-medium uppercase tracking-widest" class:text-amber-500={data.overdue_count > 0} class:text-zinc-500={data.overdue_count === 0}>Overdue</span>
				</div>
				<p class="mt-3 text-3xl font-black tracking-tight">{data.overdue_count}</p>
				<p class="mt-1 text-sm text-zinc-500">invoices past due date</p>
			</div>
		</div>

		<!-- Recovery Rate & Quick Actions -->
		<div class="mt-6 grid grid-cols-1 gap-6 lg:grid-cols-12">
			<!-- Recovery Chart -->
			<div
				class="animate-fade-in-up animation-delay-300 gradient-bg rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-6 lg:col-span-8"
			>
				<h3 class="mb-6 text-sm font-semibold uppercase tracking-widest text-zinc-500">
					Collection Overview
				</h3>
				<div class="flex items-end gap-8">
					<div>
						<p class="text-6xl font-black tracking-tighter text-emerald-400">{recoveryRate}%</p>
						<p class="mt-1 text-sm text-zinc-500">Recovery Rate</p>
					</div>
					<div class="flex flex-1 items-end gap-3">
						{#each [
							{ label: 'Total', value: data.total_invoices, max: Math.max(data.total_invoices, 1), color: 'bg-zinc-600' },
							{ label: 'Paid', value: data.total_paid > 0 ? Math.round((data.total_paid / Math.max(data.total_receivables + data.total_paid, 1)) * data.total_invoices) : 0, max: Math.max(data.total_invoices, 1), color: 'bg-emerald-500' },
							{ label: 'Overdue', value: data.overdue_count, max: Math.max(data.total_invoices, 1), color: 'bg-amber-500' }
						] as bar, i}
							<div class="flex flex-1 flex-col items-center gap-2">
								<div
									class="w-full rounded-t-lg {bar.color} transition-all duration-1000"
									style="height: {Math.max((bar.value / bar.max) * 120, 8)}px; animation-delay: {0.3 + i * 0.1}s"
								></div>
								<span class="text-xs text-zinc-500">{bar.label}</span>
							</div>
						{/each}
					</div>
				</div>
			</div>

			<!-- Quick Actions -->
			<div
				class="animate-fade-in-up animation-delay-400 gradient-bg rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-6 lg:col-span-4"
			>
				<h3 class="mb-4 text-sm font-semibold uppercase tracking-widest text-zinc-500">
					Quick Actions
				</h3>
				<div class="space-y-3">
					<a
						href="/invoices/new"
						class="flex items-center gap-3 rounded-xl border border-zinc-800 p-3 transition-colors hover:border-emerald-500/30 hover:bg-emerald-500/5"
					>
						<div class="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-500/10">
							<span class="text-emerald-400">+</span>
						</div>
						<div>
							<p class="text-sm font-medium">New Invoice</p>
							<p class="text-xs text-zinc-500">Create with AI or manually</p>
						</div>
					</a>
					<a
						href="/invoices"
						class="flex items-center gap-3 rounded-xl border border-zinc-800 p-3 transition-colors hover:border-blue-500/30 hover:bg-blue-500/5"
					>
						<div class="flex h-9 w-9 items-center justify-center rounded-lg bg-blue-500/10">
							<span class="text-blue-400">&#x1F4CB;</span>
						</div>
						<div>
							<p class="text-sm font-medium">All Invoices</p>
							<p class="text-xs text-zinc-500">View and manage</p>
						</div>
					</a>
					<a
						href="/reports"
						class="flex items-center gap-3 rounded-xl border border-zinc-800 p-3 transition-colors hover:border-zinc-700 hover:bg-zinc-800/50"
					>
						<div class="flex h-9 w-9 items-center justify-center rounded-lg bg-zinc-800">
							<span class="text-zinc-400">&#x1F4CA;</span>
						</div>
						<div>
							<p class="text-sm font-medium">Reports</p>
							<p class="text-xs text-zinc-500">Cash flow analytics</p>
						</div>
					</a>
				</div>
			</div>
		</div>
	{/if}
</div>
