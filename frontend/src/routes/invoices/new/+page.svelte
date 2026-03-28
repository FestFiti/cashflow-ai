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

	async function handleAIGenerate() {
		if (!aiPrompt.trim()) return;
		aiLoading = true;
		error = '';
		try {
			// TODO: Call AI endpoint and populate form fields
			// For now, switch to manual with a message
			error = 'AI generation coming soon — use manual mode for now';
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
</svelte:head>

<div class="mx-auto max-w-2xl px-4 py-8 md:px-8">
	<h1 class="mb-8 text-2xl font-bold tracking-tight">New Invoice</h1>

	<!-- Mode Toggle -->
	<div class="mb-6 flex rounded-xl border border-zinc-800 bg-zinc-900/30 p-1">
		<button
			onclick={() => (mode = 'ai')}
			class="flex-1 rounded-lg px-4 py-2 text-sm font-medium transition-all"
			class:bg-emerald-600={mode === 'ai'}
			class:text-white={mode === 'ai'}
			class:text-zinc-400={mode !== 'ai'}
		>
			&#x2728; AI Generate
		</button>
		<button
			onclick={() => (mode = 'manual')}
			class="flex-1 rounded-lg px-4 py-2 text-sm font-medium transition-all"
			class:bg-zinc-700={mode === 'manual'}
			class:text-white={mode === 'manual'}
			class:text-zinc-400={mode !== 'manual'}
		>
			&#x270F;&#xFE0F; Manual
		</button>
	</div>

	{#if error}
		<div class="mb-4 rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-2 text-sm text-red-400">
			{error}
		</div>
	{/if}

	{#if mode === 'ai'}
		<!-- AI Prompt -->
		<div class="gradient-bg-emerald rounded-[20px] border border-emerald-500/20 bg-emerald-500/5 p-6">
			<h3 class="mb-2 text-lg font-semibold">Describe the invoice</h3>
			<p class="mb-4 text-sm text-zinc-400">
				Type naturally — e.g. "Invoice John Kamau KES 12,000 for web design, due April 5"
			</p>
			<textarea
				bind:value={aiPrompt}
				rows={3}
				class="w-full rounded-xl border border-emerald-500/20 bg-zinc-900/50 px-4 py-3 text-sm text-white placeholder-zinc-500 outline-none focus:border-emerald-500"
				placeholder="Describe the transaction..."
			></textarea>
			<button
				onclick={handleAIGenerate}
				disabled={aiLoading || !aiPrompt.trim()}
				class="mt-4 w-full rounded-xl bg-emerald-600 py-2.5 text-sm font-semibold text-white transition-all hover:bg-emerald-500 disabled:opacity-50"
			>
				{aiLoading ? 'Generating...' : 'Generate Invoice with AI'}
			</button>
		</div>
	{:else}
		<!-- Manual Form -->
		<form onsubmit={handleSubmit} class="gradient-bg rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-6 space-y-4">
			<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
				<div>
					<label for="clientName" class="mb-1 block text-sm font-medium text-zinc-400">Client Name</label>
					<input id="clientName" type="text" bind:value={clientName} required class="w-full rounded-xl border border-zinc-700 bg-zinc-800/50 px-4 py-2.5 text-sm text-white outline-none focus:border-emerald-500" />
				</div>
				<div>
					<label for="clientPhone" class="mb-1 block text-sm font-medium text-zinc-400">Client Phone</label>
					<input id="clientPhone" type="tel" bind:value={clientPhone} required class="w-full rounded-xl border border-zinc-700 bg-zinc-800/50 px-4 py-2.5 text-sm text-white outline-none focus:border-emerald-500" placeholder="0712345678" />
				</div>
			</div>
			<div>
				<label for="clientEmail" class="mb-1 block text-sm font-medium text-zinc-400">Client Email (optional)</label>
				<input id="clientEmail" type="email" bind:value={clientEmail} class="w-full rounded-xl border border-zinc-700 bg-zinc-800/50 px-4 py-2.5 text-sm text-white outline-none focus:border-emerald-500" />
			</div>
			<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
				<div>
					<label for="amount" class="mb-1 block text-sm font-medium text-zinc-400">Amount (KES)</label>
					<input id="amount" type="number" bind:value={amount} required min="1" class="w-full rounded-xl border border-zinc-700 bg-zinc-800/50 px-4 py-2.5 text-sm text-white outline-none focus:border-emerald-500" />
				</div>
				<div>
					<label for="dueDate" class="mb-1 block text-sm font-medium text-zinc-400">Due Date</label>
					<input id="dueDate" type="date" bind:value={dueDate} required class="w-full rounded-xl border border-zinc-700 bg-zinc-800/50 px-4 py-2.5 text-sm text-white outline-none focus:border-emerald-500" />
				</div>
			</div>
			<div>
				<label for="description" class="mb-1 block text-sm font-medium text-zinc-400">Description</label>
				<textarea id="description" bind:value={description} required rows={3} class="w-full rounded-xl border border-zinc-700 bg-zinc-800/50 px-4 py-2.5 text-sm text-white outline-none focus:border-emerald-500"></textarea>
			</div>
			<button
				type="submit"
				disabled={loading}
				class="gradient-bg-emerald w-full rounded-xl bg-emerald-600 py-2.5 text-sm font-semibold text-white transition-all hover:bg-emerald-500 disabled:opacity-50"
			>
				{loading ? 'Creating...' : 'Create Invoice'}
			</button>
		</form>
	{/if}
</div>
