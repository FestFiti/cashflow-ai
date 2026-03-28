<script lang="ts">
	import { page } from '$app/stores';
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';

	interface Invoice {
		id: string;
		client_name: string;
		client_phone: string;
		client_email: string | null;
		amount: number;
		description: string;
		due_date: string;
		status: string;
		created_at: string;
	}

	let invoice = $state<Invoice | null>(null);
	let loading = $state(true);

	const statusClasses: Record<string, string> = {
		paid: 'bg-emerald-950 text-emerald-400 border-emerald-800',
		sent: 'bg-blue-950 text-blue-400 border-blue-800',
		overdue: 'bg-red-950 text-red-400 border-red-800',
		draft: 'bg-zinc-800 text-zinc-400 border-zinc-700'
	};

	onMount(async () => {
		if (!$auth.token) { goto('/login'); return; }
		try {
			invoice = await api<Invoice>(`/invoices/${$page.params.id}`, { token: $auth.token });
		} catch {
			goto('/invoices');
		} finally {
			loading = false;
		}
	});
</script>

<svelte:head>
	<title>{invoice ? `Invoice — ${invoice.client_name}` : 'Invoice'} — CashFlow AI</title>
</svelte:head>

<div class="mx-auto max-w-3xl px-4 py-8 md:px-8">
	{#if loading}
		<div class="animate-pulse space-y-4">
			<div class="h-8 w-48 rounded bg-zinc-800"></div>
			<div class="rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-6">
				<div class="h-4 w-64 rounded bg-zinc-800"></div>
			</div>
		</div>
	{:else if invoice}
		<a href="/invoices" class="mb-6 inline-flex items-center gap-1 text-sm text-zinc-400 hover:text-white">
			&larr; Back to invoices
		</a>

		<div class="gradient-bg rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-6 md:p-8">
			<div class="flex items-start justify-between">
				<div>
					<h1 class="text-2xl font-bold">{invoice.client_name}</h1>
					<p class="mt-1 text-sm text-zinc-500">{invoice.client_phone}</p>
					{#if invoice.client_email}
						<p class="text-sm text-zinc-500">{invoice.client_email}</p>
					{/if}
				</div>
				<span class="rounded-full border px-3 py-1 text-sm font-medium capitalize {statusClasses[invoice.status] || statusClasses.draft}">
					{invoice.status}
				</span>
			</div>

			<hr class="my-6 border-zinc-800" />

			<div class="grid grid-cols-2 gap-6 md:grid-cols-3">
				<div>
					<p class="text-xs font-medium uppercase tracking-widest text-zinc-500">Amount</p>
					<p class="mt-1 text-2xl font-bold">{formatKES(invoice.amount)}</p>
				</div>
				<div>
					<p class="text-xs font-medium uppercase tracking-widest text-zinc-500">Due Date</p>
					<p class="mt-1 text-lg font-semibold">{new Date(invoice.due_date).toLocaleDateString()}</p>
				</div>
				<div>
					<p class="text-xs font-medium uppercase tracking-widest text-zinc-500">Created</p>
					<p class="mt-1 text-lg font-semibold">{new Date(invoice.created_at).toLocaleDateString()}</p>
				</div>
			</div>

			<hr class="my-6 border-zinc-800" />

			<div>
				<p class="text-xs font-medium uppercase tracking-widest text-zinc-500">Description</p>
				<p class="mt-2 text-sm leading-relaxed text-zinc-300">{invoice.description}</p>
			</div>

			{#if invoice.status !== 'paid'}
				<div class="mt-8 flex gap-3">
					<button
						class="gradient-bg-emerald flex-1 rounded-xl bg-emerald-600 py-2.5 text-sm font-semibold text-white transition-all hover:bg-emerald-500"
					>
						Send M-Pesa Request
					</button>
					<button
						class="rounded-xl border border-zinc-700 px-5 py-2.5 text-sm font-medium text-zinc-300 transition-all hover:bg-zinc-800"
					>
						Download PDF
					</button>
				</div>
			{/if}
		</div>
	{/if}
</div>
