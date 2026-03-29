<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { theme } from '$lib/stores/theme';
	import Icon from '$lib/components/Icon.svelte';

	const isDark = $derived($theme === 'dark');

	interface PaymentData {
		incoming: number;
		outgoing: number;
		net_flow: number;
	}

	interface Transaction {
		id: string;
		client_name: string;
		amount: number;
		status: 'completed' | 'pending' | 'failed';
		mpesa_receipt: string | null;
		phone: string;
		paid_at: string | null;
		created_at: string | null;
	}

	let data = $state<PaymentData | null>(null);
	let transactions = $state<Transaction[]>([]);
	let loading = $state(true);
	let visible = $state(false);

	function timeAgo(dateStr: string | null): string {
		if (!dateStr) return '';
		const diff = Date.now() - new Date(dateStr).getTime();
		const mins = Math.floor(diff / 60000);
		if (mins < 1) return 'just now';
		if (mins < 60) return `${mins}m ago`;
		const hrs = Math.floor(mins / 60);
		if (hrs < 24) return `${hrs}h ago`;
		const days = Math.floor(hrs / 24);
		return `${days}d ago`;
	}

	onMount(async () => {
		if (!$auth.token) { goto('/login'); return; }
		try {
			const [statsRes, txRes] = await Promise.all([
				api<PaymentData>('/payments/stats'),
				api<Transaction[]>('/payments/')
			]);
			data = statsRes;
			transactions = txRes;
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
			default: return isDark ? 'bg-white/[0.05] text-white/60 border-white/[0.10]' : 'bg-white text-zinc-600 border-zinc-200';
		}
	}

	function getAuditStatusColor(status: string) {
		switch (status) {
			case 'completed': return 'bg-emerald-500/10 text-emerald-400';
			case 'failed': return 'bg-red-500/10 text-red-400';
			case 'pending': return 'bg-amber-500/10 text-amber-400';
			default: return isDark ? 'bg-white/[0.05] text-white/60' : 'bg-white text-zinc-600';
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
		<p class="mb-1 text-[12px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Money Movement</p>
		<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'} md:text-4xl">Payments</h1>
		<p class="mt-2 text-[15px] {isDark ? 'text-white/40' : 'text-zinc-500'}">Inflows • Outflows • Activity</p>
	</div>

	{#if loading}
		<!-- Skeleton -->
		<div class="grid grid-cols-1 gap-4 md:grid-cols-3">
			{#each Array(3) as _}
				<div class="animate-pulse rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6">
					<div class="mb-3 h-3 w-20 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-200'}"></div>
					<div class="h-8 w-28 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-200'}"></div>
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
				<p class="text-2xl font-bold tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">{formatKES(data.incoming)}</p>
				<p class="mt-2 text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Money received</p>
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
				<p class="text-2xl font-bold tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">{formatKES(data.outgoing)}</p>
				<p class="mt-2 text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Payments made</p>
			</div>

			<!-- Net Flow -->
			<div class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6 transition-all duration-500 delay-150 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-4 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Net Flow</span>
					<div class="flex h-8 w-8 items-center justify-center rounded-lg {isDark ? 'bg-white/[0.03]' : 'bg-white'}">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {isDark ? 'text-white/30' : 'text-zinc-500'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M3 13.125C3 12.504 3.504 12 4.125 12h2.25c.621 0 1.125.504 1.125 1.125v6.75C7.5 20.496 6.996 21 6.375 21h-2.25A1.125 1.125 0 013 19.875v-6.75zM9.75 8.625c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125v11.25c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V8.625zM16.5 4.125c0-.621.504-1.125 1.125-1.125h2.25C20.496 3 21 3.504 21 4.125v15.75c0 .621-.504 1.125-1.125 1.125h-2.25a1.125 1.125 0 01-1.125-1.125V4.125z" />
						</svg>
					</div>
				</div>
				<p class="text-2xl font-bold tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">{formatKES(data.net_flow)}</p>
				<p class="mt-2 text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Net movement</p>
			</div>
		</div>

		<!-- Bottom Row -->
		<div class="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-12">
			<!-- Main Content -->
			<div class="space-y-6 lg:col-span-8">
				<!-- Quick Actions -->
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6 transition-all duration-500 delay-200 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Quick Actions</span>
					<div class="grid grid-cols-1 gap-3 md:grid-cols-2">
						<a
							href="/payments/request"
							class="group rounded-xl border border-emerald-500/20 bg-emerald-500/[0.03] p-4 transition-all hover:border-emerald-500/40 hover:bg-emerald-500/[0.05]"
						>
							<div class="flex items-start gap-3">
								<div class="flex h-10 w-10 items-center justify-center rounded-lg bg-emerald-500/10">
									<Icon name="request-payment" stroke="rgba(52,211,153,1)" />
								</div>
								<div>
									<p class="text-[13px] font-semibold text-emerald-400">Request Payment</p>
									<p class="mt-1 text-[11px] {isDark ? 'text-white/40' : 'text-zinc-500'}">Collect via M-Pesa or payment link</p>
								</div>
							</div>
						</a>

						<a
							href="/payments/send"
							class="group rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-4 transition-all {isDark ? 'hover:border-white/[0.08] hover:bg-white/[0.05]' : 'hover:border-zinc-300 hover:bg-zinc-50'}"
						>
							<div class="flex items-start gap-3">
								<div class="flex h-10 w-10 items-center justify-center rounded-lg {isDark ? 'bg-white/[0.03]' : 'bg-zinc-100'}">
									<Icon name="send-money" stroke={isDark ? 'rgba(255,255,255,0.4)' : 'rgba(113,113,122,1)'} />
								</div>
								<div>
									<p class="text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Send Money</p>
									<p class="mt-1 text-[11px] {isDark ? 'text-white/40' : 'text-zinc-500'}">Pay suppliers or customers</p>
								</div>
							</div>
						</a>

						<a
							href="/payments/record"
							class="group rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-4 transition-all {isDark ? 'hover:border-white/[0.08] hover:bg-white/[0.05]' : 'hover:border-zinc-300 hover:bg-zinc-50'}"
						>
							<div class="flex items-start gap-3">
								<div class="flex h-10 w-10 items-center justify-center rounded-lg {isDark ? 'bg-white/[0.03]' : 'bg-zinc-100'}">
									<Icon name="record-payment" stroke={isDark ? 'rgba(255,255,255,0.4)' : 'rgba(113,113,122,1)'} />
								</div>
								<div>
									<p class="text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Record Payment</p>
									<p class="mt-1 text-[11px] {isDark ? 'text-white/40' : 'text-zinc-500'}">Log external or cash payments</p>
								</div>
							</div>
						</a>

						<button class="group rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-4 transition-all {isDark ? 'hover:border-white/[0.08] hover:bg-white/[0.05]' : 'hover:border-zinc-300 hover:bg-zinc-50'}">
							<div class="flex items-start gap-3">
								<div class="flex h-10 w-10 items-center justify-center rounded-lg {isDark ? 'bg-white/[0.03]' : 'bg-zinc-100'}">
									<Icon name="request-payment" stroke={isDark ? 'rgba(255,255,255,0.4)' : 'rgba(113,113,122,1)'} />
								</div>
								<div>
									<p class="text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Bulk STK Push</p>
									<p class="mt-1 text-[11px] {isDark ? 'text-white/40' : 'text-zinc-500'}">Send multiple payment requests at once</p>
								</div>
							</div>
						</button>
					</div>
				</div>

				<!-- Transactions Feed -->
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6 transition-all duration-500 delay-300 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<div class="mb-6 flex items-center justify-between">
						<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Activity</span>
						<div class="flex items-center gap-2">
							<span class="h-2 w-2 rounded-full bg-emerald-400 animate-pulse"></span>
							<span class="text-[10px] {isDark ? 'text-white/40' : 'text-zinc-500'}">Live</span>
						</div>
					</div>

					{#if transactions.length === 0}
						<div class="text-center py-12">
							<div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full {isDark ? 'bg-white/[0.05]' : 'bg-white'}">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 {isDark ? 'text-white/30' : 'text-zinc-500'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
									<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 8.25h19.5M2.25 9h19.5m-16.5 5.25h6m-6 2.25h3m-3.75 3h15a2.25 2.25 0 002.25-2.25V6.75A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25v10.5A2.25 2.25 0 004.5 19.5z" />
								</svg>
							</div>
							<p class="text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'}">No payment activity yet</p>
							<p class="mt-1 text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Payments will appear here when clients pay via M-Pesa</p>
						</div>
					{:else}
						<div class="space-y-3">
							{#each transactions as tx}
								<div class="rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.01]' : 'border-zinc-200 bg-white'} p-4 transition-all {isDark ? 'hover:border-white/[0.08]' : 'hover:border-zinc-300'}">
									<div class="flex items-center justify-between">
										<div class="flex items-center gap-3">
											<div class="flex h-10 w-10 items-center justify-center rounded-full {isDark ? 'bg-white/[0.05]' : 'bg-white'}">
												<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
													<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m6-6H6" />
												</svg>
											</div>
											<div>
												<p class="text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">{tx.client_name}</p>
												<p class="text-[11px] {isDark ? 'text-white/40' : 'text-zinc-500'}">
													{tx.mpesa_receipt ?? 'M-Pesa'} • {timeAgo(tx.paid_at ?? tx.created_at)}
												</p>
											</div>
										</div>
										<div class="text-right">
											<p class="text-lg font-medium text-emerald-400">+{formatKES(tx.amount)}</p>
											<span class="inline-block mt-1 rounded-full px-2 py-0.5 text-[10px] font-medium {getStatusColor(tx.status)}">
												{tx.status}
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
				<!-- Summary -->
				<div class="rounded-2xl border border-emerald-500/10 bg-emerald-500/[0.03] p-6 transition-all duration-500 delay-400 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<div class="mb-4 flex items-center gap-2">
						<div class="flex h-6 w-6 items-center justify-center rounded-full bg-emerald-400">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
							</svg>
						</div>
						<span class="text-[11px] font-medium text-emerald-400">Summary</span>
					</div>
					<div class="space-y-3">
						<div class="flex items-start gap-2">
							<span class="mt-1 h-1 w-1 rounded-full bg-emerald-400"></span>
							<p class="text-[12px] {isDark ? 'text-white/60' : 'text-zinc-600'}">{transactions.filter(t => t.status === 'completed').length} completed payments</p>
						</div>
						<div class="flex items-start gap-2">
							<span class="mt-1 h-1 w-1 rounded-full bg-amber-400"></span>
							<p class="text-[12px] {isDark ? 'text-white/60' : 'text-zinc-600'}">{transactions.filter(t => t.status === 'pending').length} pending</p>
						</div>
						<div class="flex items-start gap-2">
							<span class="mt-1 h-1 w-1 rounded-full bg-red-400"></span>
							<p class="text-[12px] {isDark ? 'text-white/60' : 'text-zinc-600'}">{transactions.filter(t => t.status === 'failed').length} failed</p>
						</div>
					</div>
				</div>

				<!-- Audit Trail -->
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6 transition-all duration-500 delay-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Audit Trail</span>
					{#if transactions.length === 0}
						<p class="text-[12px] {isDark ? 'text-white/30' : 'text-zinc-400'}">No activity to show</p>
					{:else}
						<div class="space-y-3">
							{#each transactions.slice(0, 8) as tx}
								<div class="flex items-start gap-3">
									<div class="mt-0.5 flex h-2 w-2 flex-shrink-0 rounded-full {getAuditStatusColor(tx.status)}"></div>
									<div class="flex-1">
										<p class="text-[12px] {isDark ? 'text-white/60' : 'text-zinc-600'}">
											{#if tx.status === 'completed'}
												Payment confirmed from {tx.client_name} — {tx.mpesa_receipt ?? 'M-Pesa'}
											{:else if tx.status === 'pending'}
												STK Push sent to {tx.phone}
											{:else}
												Payment failed for {tx.client_name}
											{/if}
										</p>
										<p class="mt-1 text-[10px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{timeAgo(tx.paid_at ?? tx.created_at)}</p>
									</div>
								</div>
							{/each}
						</div>
					{/if}
				</div>
			</div>
		</div>
	{/if}
</div>
