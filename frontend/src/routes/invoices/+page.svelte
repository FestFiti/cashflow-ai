<script lang="ts">
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { theme } from '$lib/stores/theme';
	import { getAvatarUrl } from '$lib/avatar';

	const isDark = $derived($theme === 'dark');

	interface Invoice {
		id: string;
		client_name: string;
		client_phone: string;
		amount: number;
		description: string;
		due_date: string;
		status: string;
		created_at: string;
	}

	let invoices = $state<Invoice[]>([]);
	let loading = $state(true);
	let visible = $state(false);

	onMount(async () => {
		if (!$auth.token) { goto('/login'); return; }
		try {
			invoices = await api<Invoice[]>('/invoices/', { token: $auth.token });
		} catch {
			invoices = [];
		} finally {
			loading = false;
			setTimeout(() => (visible = true), 50);
		}
	});

	function statusColor(status: string) {
		switch (status) {
			case 'paid': return 'border-emerald-500/20 bg-emerald-500/10 text-emerald-400';
			case 'sent': return 'border-blue-500/20 bg-blue-500/10 text-blue-400';
			case 'overdue': return 'border-amber-500/20 bg-amber-500/10 text-amber-400';
			default: return `${isDark ? 'border-white/[0.08]' : 'border-zinc-200'} ${isDark ? 'bg-white/[0.03]' : 'bg-white'} ${isDark ? 'text-white/40' : 'text-zinc-500'}`;
		}
	}

	function statusIcon(status: string) {
		switch (status) {
			case 'paid': return 'M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z';
			case 'sent': return 'M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5';
			case 'overdue': return 'M12 9v3.75m9-.75a9 9 0 11-18 0 9 9 0 0118 0zm-9 3.75h.008v.008H12v-.008z';
			default: return 'M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z';
		}
	}
</script>

<svelte:head>
	<title>Invoices — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<!-- Header -->
	<div class="mb-8 flex items-end justify-between">
		<div>
			<p class="mb-1 text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Billing</p>
			<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'} md:text-4xl">
				<span class="italic text-emerald-400">Invoices</span>
			</h1>
		</div>
		<a
			href="/invoices/new"
			class="group inline-flex items-center gap-2 rounded-xl bg-emerald-500 px-5 py-2.5 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400"
		>
			<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
			</svg>
			New Invoice
		</a>
	</div>

	{#if loading}
		<!-- Skeleton -->
		<div class="space-y-3">
			{#each Array(4) as _}
				<div class="animate-pulse rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-5">
					<div class="flex items-center justify-between">
						<div class="flex items-center gap-4">
							<div class="h-10 w-10 rounded-lg {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
							<div>
								<div class="mb-2 h-3.5 w-32 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
								<div class="h-3 w-48 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
							</div>
						</div>
						<div class="text-right">
							<div class="mb-2 h-3.5 w-24 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
							<div class="h-3 w-16 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
						</div>
					</div>
				</div>
			{/each}
		</div>
	{:else if invoices.length === 0}
		<!-- Empty State -->
		<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-12 text-center transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<div class="mx-auto flex h-14 w-14 items-center justify-center rounded-lg {isDark ? 'bg-white/[0.03]' : 'bg-white'}">
				<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 {isDark ? 'text-white/20' : 'text-zinc-400'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
					<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
				</svg>
			</div>
			<h3 class="mt-5 font-['Instrument_Serif'] text-xl {isDark ? 'text-white' : 'text-zinc-900'}">No invoices yet</h3>
			<p class="mt-2 text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Create your first invoice to start tracking payments</p>
			<a
				href="/invoices/new"
				class="mt-6 inline-flex items-center gap-2 rounded-xl bg-emerald-500 px-6 py-2.5 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400"
			>
				<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
				</svg>
				Create Invoice
			</a>
		</div>
	{:else}
		<!-- Invoice List -->
		<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<!-- Table Header -->
			<div class="hidden border-b {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} px-5 py-3 md:grid md:grid-cols-12 md:gap-4">
				<span class="col-span-5 text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Client</span>
				<span class="col-span-3 text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Amount</span>
				<span class="col-span-2 text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Due Date</span>
				<span class="col-span-2 text-right text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Status</span>
			</div>

			{#each invoices as invoice, i}
				<a
					href="/invoices/{invoice.id}"
					class="group flex flex-col gap-3 border-b {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} px-5 py-4 transition-all {isDark ? 'hover:bg-white/[0.02]' : 'hover:bg-zinc-50'} md:grid md:grid-cols-12 md:items-center md:gap-4 last:border-b-0"
					style="transition-delay: {i * 40}ms;"
				>
					<!-- Client -->
					<div class="col-span-5 flex items-center gap-3">
						<img src={getAvatarUrl(invoice.client_name)} alt={invoice.client_name} class="h-9 w-9 shrink-0 rounded-lg" />
						<div class="min-w-0">
							<p class="truncate text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">{invoice.client_name}</p>
							<p class="truncate text-[12px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{invoice.description}</p>
						</div>
					</div>

					<!-- Amount -->
					<div class="col-span-3">
						<p class="text-[13px] font-semibold {isDark ? 'text-white' : 'text-zinc-900'}">{formatKES(invoice.amount)}</p>
					</div>

					<!-- Due Date -->
					<div class="col-span-2">
						<p class="text-[12px] {isDark ? 'text-white/25' : 'text-zinc-400'}">{new Date(invoice.due_date).toLocaleDateString()}</p>
					</div>

					<!-- Status -->
					<div class="col-span-2 flex justify-end">
						<span class="inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[11px] font-medium capitalize {statusColor(invoice.status)}">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d={statusIcon(invoice.status)} />
							</svg>
							{invoice.status}
						</span>
					</div>
				</a>
			{/each}
		</div>
	{/if}
</div>
