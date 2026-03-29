<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	interface PaymentData {
		incoming: number;
		outgoing: number;
		net_flow: number;
	}

	interface Transaction {
		id: number;
		name: string;
		amount: number;
		type: 'incoming' | 'outgoing';
		status: 'completed' | 'pending' | 'failed';
		timestamp: string;
	}

	interface AuditTrail {
		id: number;
		description: string;
		timestamp: string;
		status: 'success' | 'error' | 'info';
	}

	let data = $state<PaymentData | null>(null);
	let loading = $state(true);
	let visible = $state(false);

	// Mock data
	let transactions = $state<Transaction[]>([
		{ id: 1, name: 'Mary Wanjiku', amount: 5000, type: 'incoming', status: 'completed', timestamp: '2 mins ago' },
		{ id: 2, name: 'Supplier Payment', amount: 2000, type: 'outgoing', status: 'completed', timestamp: '15 mins ago' },
		{ id: 3, name: 'John Kamau', amount: 3500, type: 'incoming', status: 'pending', timestamp: '30 mins ago' },
		{ id: 4, name: 'Office Supplies', amount: 1500, type: 'outgoing', status: 'failed', timestamp: '1 hour ago' },
		{ id: 5, name: 'Grace Njeri', amount: 8000, type: 'incoming', status: 'completed', timestamp: '2 hours ago' }
	]);

	let auditTrail = $state<AuditTrail[]>([
		{ id: 1, description: 'STK Push initiated to 0712345678', timestamp: '2 mins ago', status: 'info' },
		{ id: 2, description: 'Payment confirmed from M-Pesa callback', timestamp: '15 mins ago', status: 'success' },
		{ id: 3, description: 'Payment failed - insufficient funds', timestamp: '1 hour ago', status: 'error' },
		{ id: 4, description: 'Manual payment recorded - Cash transaction', timestamp: '2 hours ago', status: 'success' },
		{ id: 5, description: 'Bulk STK push sent to 5 recipients', timestamp: '3 hours ago', status: 'success' }
	]);

	let insights = $state([
		'You received KES 25,000 today',
		'Outgoing payments increased this week',
		'2 payments are still pending'
	]);

	onMount(async () => {
		if (!$auth.token) { goto('/login'); return; }
		try {
			// TODO: Fetch actual payment data
			data = {
				incoming: 25000,
				outgoing: 12000,
				net_flow: 13000
			};
		} catch {
			data = { incoming: 0, outgoing: 0, net_flow: 0 };
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
			default: return 'bg-white/[0.05] text-white/60 border-white/[0.10]';
		}
	}

	function getAuditStatusColor(status: string) {
		switch (status) {
			case 'success': return 'bg-emerald-500/10 text-emerald-400';
			case 'error': return 'bg-red-500/10 text-red-400';
			case 'info': return 'bg-blue-500/10 text-blue-400';
			default: return 'bg-white/[0.05] text-white/60';
		}
	}

	function getTypeColor(type: string) {
		switch (type) {
			case 'incoming': return 'text-emerald-400';
			case 'outgoing': return 'text-red-400';
			default: return 'text-white/60';
		}
	}
</script>

<svelte:head>
	<title>Payments — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<!-- Header -->
	<div class="mb-8">
		<p class="mb-1 text-[12px] font-medium uppercase tracking-[0.15em] text-white/25">Money Movement</p>
		<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight text-white md:text-4xl">Payments</h1>
		<p class="mt-2 text-[15px] text-white/40">Inflows • Outflows • Activity</p>
	</div>

	{#if loading}
		<!-- Skeleton -->
		<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
			{#each Array(3) as _}
				<div class="animate-pulse rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6">
					<div class="mb-3 h-3 w-20 rounded bg-white/[0.04]"></div>
					<div class="h-8 w-28 rounded bg-white/[0.04]"></div>
				</div>
			{/each}
		</div>
	{:else if data}
		<!-- Top Summary Cards -->
		<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
			<!-- Incoming -->
			<div class="rounded-2xl border border-emerald-500/10 bg-emerald-500/[0.03] p-6 transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-4 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] text-emerald-500/70">Incoming</span>
					<div class="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-500/10">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m6-6H6" />
						</svg>
					</div>
				</div>
				<p class="text-2xl font-bold tracking-tight text-white">{formatKES(data.incoming)}</p>
				<p class="mt-2 text-[11px] text-white/20">Money received</p>
			</div>

			<!-- Outgoing -->
			<div class="rounded-2xl border border-red-500/10 bg-red-500/[0.03] p-6 transition-all duration-500 delay-75 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-4 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] text-red-500/70">Outgoing</span>
					<div class="flex h-8 w-8 items-center justify-center rounded-lg bg-red-500/10">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m6-6H6" />
						</svg>
					</div>
				</div>
				<p class="text-2xl font-bold tracking-tight text-white">{formatKES(data.outgoing)}</p>
				<p class="mt-2 text-[11px] text-white/20">Payments made</p>
			</div>

			<!-- Net Flow -->
			<div class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6 transition-all duration-500 delay-150 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-4 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Net Flow</span>
					<div class="flex h-8 w-8 items-center justify-center rounded-lg bg-white/[0.03]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-white/30" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
						</svg>
					</div>
				</div>
				<p class="text-2xl font-bold tracking-tight text-white">{formatKES(data.net_flow)}</p>
				<p class="mt-2 text-[11px] text-white/20">Net movement</p>
			</div>
		</div>

		<!-- Bottom Row -->
		<div class="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-12">
			<!-- Main Content -->
			<div class="space-y-6 lg:col-span-8">
				<!-- Quick Actions -->
				<div class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6 transition-all duration-500 delay-200 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Quick Actions</span>
					<div class="grid grid-cols-1 gap-3 md:grid-cols-2">
						<a
							href="/payments/request"
							class="group rounded-xl border border-emerald-500/20 bg-emerald-500/[0.03] p-4 transition-all hover:border-emerald-500/40 hover:bg-emerald-500/[0.05]"
						>
							<div class="flex items-start gap-3">
								<div class="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-500/10">
									<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
										<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" />
									</svg>
								</div>
								<div>
									<p class="text-[13px] font-semibold text-emerald-400">Request Payment</p>
									<p class="mt-1 text-[11px] text-white/40">Collect via M-Pesa or payment link</p>
								</div>
							</div>
						</a>

						<a
							href="/payments/send"
							class="group rounded-xl border border-white/[0.04] bg-white/[0.02] p-4 transition-all hover:border-white/[0.08] hover:bg-white/[0.05]"
						>
							<div class="flex items-start gap-3">
								<div class="flex h-10 w-10 items-center justify-center rounded-lg bg-white/[0.03]">
									<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white/30" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
										<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m6-6H6" />
									</svg>
								</div>
								<div>
									<p class="text-[13px] font-medium text-white/80">Send Money</p>
									<p class="mt-1 text-[11px] text-white/40">Pay suppliers or customers</p>
								</div>
							</div>
						</a>

						<a
							href="/payments/record"
							class="group rounded-xl border border-white/[0.04] bg-white/[0.02] p-4 transition-all hover:border-white/[0.08] hover:bg-white/[0.05]"
						>
							<div class="flex items-start gap-3">
								<div class="flex h-10 w-10 items-center justify-center rounded-lg bg-white/[0.03]">
									<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white/30" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
										<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.745 3.745 0 011.043 3.296A3.745 3.745 0 0121 12z" />
									</svg>
								</div>
								<div>
									<p class="text-[13px] font-medium text-white/80">Record Payment</p>
									<p class="mt-1 text-[11px] text-white/40">Log external or cash payments</p>
								</div>
							</div>
						</a>

						<button class="group rounded-xl border border-white/[0.04] bg-white/[0.02] p-4 transition-all hover:border-white/[0.08] hover:bg-white/[0.05]">
							<div class="flex items-start gap-3">
								<div class="flex h-10 w-10 items-center justify-center rounded-lg bg-white/[0.03]">
									<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white/30" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
										<path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197A5.971 5.971 0 006 18.72v-2.007m0 0V18.72v-2.007m0 0a5.971 5.971 0 00-.941 3.197M5.058 15.522A5.971 5.971 0 006 18.72v-2.007M5.058 15.522A5.971 5.971 0 016 12.75v2.007m0 0a5.971 5.971 0 00.941 3.197m8.018-8.018a5.971 5.971 0 00-.941-3.197M6 12.75a5.971 5.971 0 01.941-3.197m5.059 5.059a5.971 5.971 0 01-.941 3.197M12 12.75a5.971 5.971 0 01-.941-3.197m0 6.394a5.971 5.971 0 00.941-3.197m0-6.394a5.971 5.971 0 00-.941 3.197" />
									</svg>
								</div>
								<div>
									<p class="text-[13px] font-medium text-white/80">Bulk STK Push</p>
									<p class="mt-1 text-[11px] text-white/40">Send multiple payment requests at once</p>
								</div>
							</div>
						</button>
					</div>
				</div>

				<!-- Transactions Feed -->
				<div class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6 transition-all duration-500 delay-300 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<div class="mb-6 flex items-center justify-between">
						<span class="text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Activity</span>
						<div class="flex items-center gap-2">
							<span class="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
							<span class="text-[10px] text-white/40">Live</span>
						</div>
					</div>

					{#if transactions.length === 0}
						<div class="text-center py-12">
							<div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-white/[0.05]">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-white/30" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
									<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" />
								</svg>
							</div>
							<p class="text-[13px] text-white/40">No payment activity yet</p>
						</div>
					{:else}
						<div class="space-y-3">
							{#each transactions as transaction}
								<div class="rounded-xl border border-white/[0.04] bg-white/[0.01] p-4 transition-all hover:border-white/[0.08]">
									<div class="flex items-center justify-between">
										<div class="flex items-center gap-3">
											<div class="flex h-10 w-10 items-center justify-center rounded-full bg-white/[0.05]">
												<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {getTypeColor(transaction.type)}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
													{#if transaction.type === 'incoming'}
														<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m6-6H6" />
													{:else}
														<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m6-6H6" />
													{/if}
												</svg>
											</div>
											<div>
												<p class="text-[13px] font-medium text-white/80">{transaction.name}</p>
												<p class="text-[11px] text-white/40">{transaction.type} • {transaction.timestamp}</p>
											</div>
										</div>
										<div class="text-right">
											<p class="text-lg font-medium {getTypeColor(transaction.type)}">
												{transaction.type === 'incoming' ? '+' : '-'}{formatKES(transaction.amount)}
											</p>
											<span class="inline-block mt-1 rounded-full px-2 py-0.5 text-[10px] font-medium {getStatusColor(transaction.status)}">
												{transaction.status}
											</span>
										</div>
									</div>
								</div>
							{/each}
						</div>
					{/if}
				</div>
			</div>

			<!-- Sidebar -->
			<div class="space-y-6 lg:col-span-4">
				<!-- Intelligence Panel -->
				<div class="rounded-2xl border border-emerald-500/10 bg-emerald-500/[0.03] p-6 transition-all duration-500 delay-400 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<div class="mb-4 flex items-center gap-2">
						<div class="flex h-6 w-6 items-center justify-center rounded-full bg-emerald-400">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
							</svg>
						</div>
						<span class="text-[11px] font-medium text-emerald-400">Intelligence</span>
					</div>
					<div class="space-y-3">
						{#each insights as insight}
							<div class="flex items-start gap-2">
								<span class="mt-1 h-1 w-1 rounded-full bg-emerald-400"></span>
								<p class="text-[12px] text-white/60">{insight}</p>
							</div>
						{/each}
					</div>
				</div>

				<!-- Audit Trail -->
				<div class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6 transition-all duration-500 delay-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Audit Trail</span>
					<div class="space-y-3">
						{#each auditTrail as audit}
							<div class="flex items-start gap-3">
								<div class="mt-0.5 flex h-2 w-2 flex-shrink-0 rounded-full {getAuditStatusColor(audit.status)}"></div>
								<div class="flex-1">
									<p class="text-[12px] text-white/60">{audit.description}</p>
									<p class="mt-1 text-[10px] text-white/20">{audit.timestamp}</p>
								</div>
							</div>
						{/each}
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>
