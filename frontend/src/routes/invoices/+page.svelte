<script lang="ts">
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';

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

	onMount(async () => {
		if (!$auth.token) { goto('/login'); return; }
		try {
			invoices = await api<Invoice[]>('/invoices/', { token: $auth.token });
		} catch {
			invoices = [];
		} finally {
			loading = false;
		}
	});

	function statusColor(status: string) {
		switch (status) {
			case 'paid': return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20';
			case 'sent': return 'bg-blue-500/10 text-blue-400 border-blue-500/20';
			case 'overdue': return 'bg-red-500/10 text-red-400 border-red-500/20';
			default: return 'bg-zinc-500/10 text-zinc-400 border-zinc-500/20';
		}
	}
</script>

<svelte:head>
	<title>Invoices — CashFlow AI</title>
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8">
	<div class="mb-8 flex items-center justify-between">
		<h1 class="text-2xl font-bold tracking-tight">Invoices</h1>
		<a
			href="/invoices/new"
			class="gradient-bg-emerald inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-5 py-2.5 text-sm font-semibold text-white transition-all hover:bg-emerald-500"
		>
			<span>+</span> New Invoice
		</a>
	</div>

	{#if loading}
		<div class="space-y-4">
			{#each Array(3) as _}
				<div class="animate-pulse rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-5">
					<div class="flex items-center justify-between">
						<div class="h-4 w-32 rounded bg-zinc-800"></div>
						<div class="h-4 w-20 rounded bg-zinc-800"></div>
					</div>
				</div>
			{/each}
		</div>
	{:else if invoices.length === 0}
		<div class="gradient-bg rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-12 text-center">
			<p class="text-4xl">&#x1F4DD;</p>
			<h3 class="mt-4 text-lg font-semibold">No invoices yet</h3>
			<p class="mt-2 text-sm text-zinc-500">Create your first invoice to get started</p>
			<a
				href="/invoices/new"
				class="mt-6 inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-6 py-2.5 text-sm font-semibold text-white hover:bg-emerald-500"
			>
				Create Invoice
			</a>
		</div>
	{:else}
		<div class="space-y-3">
			{#each invoices as invoice, i}
				<a
					href="/invoices/{invoice.id}"
					class="animate-fade-in-up gradient-bg flex items-center justify-between rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-5 transition-all hover:border-zinc-700"
					style="animation-delay: {i * 0.05}s"
				>
					<div class="flex items-center gap-4">
						<div class="flex h-10 w-10 items-center justify-center rounded-xl bg-zinc-800 text-sm font-bold text-zinc-400">
							{invoice.client_name.charAt(0)}
						</div>
						<div>
							<p class="font-semibold">{invoice.client_name}</p>
							<p class="text-sm text-zinc-500">{invoice.description}</p>
						</div>
					</div>
					<div class="flex items-center gap-4">
						<div class="text-right">
							<p class="font-semibold">{formatKES(invoice.amount)}</p>
							<p class="text-xs text-zinc-500">Due {new Date(invoice.due_date).toLocaleDateString()}</p>
						</div>
						<span class="rounded-full border px-2.5 py-0.5 text-xs font-medium capitalize {statusColor(invoice.status)}">
							{invoice.status}
						</span>
					</div>
				</a>
			{/each}
		</div>
	{/if}
</div>
