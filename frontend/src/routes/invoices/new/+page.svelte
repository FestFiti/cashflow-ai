<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api } from '$lib/api';
	import { goto } from '$app/navigation';

	let mode = $state<'manual' | 'ai'>('ai');
	let aiPrompt = $state('');
	let aiLoading = $state(false);

	// Manual form fields
	let clientName = $state('');
	let clientPhone = $state('');
	let clientEmail = $state('');
	let amount = $state('');
	let description = $state('');
	let dueDate = $state('');
	let error = $state('');
	let loading = $state(false);
	let visible = $state(false);

	import { onMount } from 'svelte';
	onMount(() => {
		if (!$auth.token) { goto('/login'); return; }
		setTimeout(() => (visible = true), 50);
	});

	async function handleAIGenerate() {
		if (!aiPrompt.trim()) return;
		aiLoading = true;
		error = '';
		try {
			// TODO: Call AI endpoint and populate form fields
			// For now, switch to manual with a message
			error = 'AI generation coming soon -- use manual mode for now';
			mode = 'manual';
		} finally {
			aiLoading = false;
		}
	}

	async function handleSubmit(e: Event) {
		e.preventDefault();
		error = '';
		loading = true;
		try {
			await api('/invoices/', {
				method: 'POST',
				token: $auth.token!,
				body: JSON.stringify({
					client_name: clientName,
					client_phone: clientPhone,
					client_email: clientEmail || null,
					amount: parseFloat(amount),
					description,
					due_date: dueDate
				})
			});
			goto('/invoices');
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to create invoice';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>New Invoice — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-2xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<!-- Back link -->
	<a href="/invoices" class="mb-6 inline-flex items-center gap-1.5 text-[13px] text-white/25 transition-colors hover:text-white/50">
		<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
			<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
		</svg>
		Back to invoices
	</a>

	<!-- Header -->
	<div class="mb-8">
		<p class="mb-1 text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Create</p>
		<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight text-white">
			New <span class="italic text-emerald-400">Invoice</span>
		</h1>
	</div>

	<!-- Mode Toggle -->
	<div class="mb-6 flex rounded-xl border border-white/[0.04] bg-white/[0.02] p-1 transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
		<button
			onclick={() => (mode = 'ai')}
			class="flex flex-1 items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-[13px] font-medium transition-all {mode === 'ai' ? 'bg-emerald-500 text-zinc-950' : 'text-zinc-500'}"
		>
			<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
				<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
			</svg>
			AI Generate
		</button>
		<button
			onclick={() => (mode = 'manual')}
			class="flex flex-1 items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-[13px] font-medium transition-all {mode === 'manual' ? 'bg-zinc-800 text-white' : 'text-zinc-500'}"
		>
			<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
				<path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
			</svg>
			Manual
		</button>
	</div>

	{#if error}
		<div class="mb-4 rounded-xl border border-red-500/20 bg-red-500/[0.05] px-4 py-3 text-[13px] text-red-400">
			{error}
		</div>
	{/if}

	{#if mode === 'ai'}
		<!-- AI Prompt -->
		<div class="rounded-2xl border border-emerald-500/10 bg-emerald-500/[0.03] p-6 transition-all duration-500 delay-75 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<div class="mb-4 flex items-center gap-3">
				<div class="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-500/10">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
					</svg>
				</div>
				<div>
					<h3 class="text-[14px] font-semibold text-white/80">Describe the invoice</h3>
					<p class="text-[12px] text-white/20">Type naturally -- e.g. "Invoice John Kamau KES 12,000 for web design, due April 5"</p>
				</div>
			</div>
			<textarea
				bind:value={aiPrompt}
				rows={3}
				class="w-full rounded-xl border border-emerald-500/10 bg-white/[0.02] px-4 py-3 text-[13px] text-white placeholder-white/15 outline-none transition-colors focus:border-emerald-500/30"
				placeholder="Describe the transaction..."
			></textarea>
			<button
				onclick={handleAIGenerate}
				disabled={aiLoading || !aiPrompt.trim()}
				class="mt-4 w-full rounded-xl bg-emerald-500 py-2.5 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400 disabled:opacity-40"
			>
				{aiLoading ? 'Generating...' : 'Generate Invoice with AI'}
			</button>
		</div>
	{:else}
		<!-- Manual Form -->
		<form onsubmit={handleSubmit} class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6 transition-all duration-500 delay-75 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<div class="space-y-5">
				<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
					<div>
						<label for="clientName" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Client Name</label>
						<input id="clientName" type="text" bind:value={clientName} required class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none transition-colors placeholder-white/15 focus:border-emerald-500/30" />
					</div>
					<div>
						<label for="clientPhone" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Client Phone</label>
						<input id="clientPhone" type="tel" bind:value={clientPhone} required class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none transition-colors placeholder-white/15 focus:border-emerald-500/30" placeholder="0712345678" />
					</div>
				</div>
				<div>
					<label for="clientEmail" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Client Email <span class="normal-case tracking-normal text-white/15">(optional)</span></label>
					<input id="clientEmail" type="email" bind:value={clientEmail} class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none transition-colors placeholder-white/15 focus:border-emerald-500/30" />
				</div>
				<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
					<div>
						<label for="amount" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Amount (KES)</label>
						<input id="amount" type="number" bind:value={amount} required min="1" class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none transition-colors placeholder-white/15 focus:border-emerald-500/30" />
					</div>
					<div>
						<label for="dueDate" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Due Date</label>
						<input id="dueDate" type="date" bind:value={dueDate} required class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none transition-colors placeholder-white/15 focus:border-emerald-500/30" />
					</div>
				</div>
				<div>
					<label for="description" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Description</label>
					<textarea id="description" bind:value={description} required rows={3} class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none transition-colors placeholder-white/15 focus:border-emerald-500/30"></textarea>
				</div>
			</div>
			<button
				type="submit"
				disabled={loading}
				class="mt-6 w-full rounded-xl bg-emerald-500 py-2.5 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400 disabled:opacity-40"
			>
				{loading ? 'Creating...' : 'Create Invoice'}
			</button>
		</form>
	{/if}
</div>
