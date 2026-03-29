<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let mode = $state<'manual' | 'ai'>('ai');
	let aiPrompt = $state('');
	let aiLoading = $state(false);

	let clientName = $state('');
	let clientPhone = $state('');
	let clientEmail = $state('');
	let amount = $state('');
	let description = $state('');
	let dueDate = $state('');
	let paymentMethod = $state('mpesa');
	let error = $state('');
	let loading = $state(false);
	let visible = $state(false);

	onMount(() => {
		if (!$auth.token) { goto('/login'); return; }
		setTimeout(() => (visible = true), 50);
	});

	const parsedAmount = $derived(parseFloat(amount) || 0);
	const hasPreviewData = $derived(clientName || parsedAmount > 0 || description);

	async function handleAIGenerate() {
		if (!aiPrompt.trim()) return;
		aiLoading = true;
		error = '';
		try {
			const res = await api<{ status: string; invoice: any }>('/ai/generate-invoice', {
				method: 'POST',
				body: JSON.stringify({ prompt: aiPrompt })
			});
			if (res.invoice) {
				clientName = res.invoice.client_name || '';
				clientPhone = res.invoice.client_phone || '';
				clientEmail = res.invoice.client_email || '';
				amount = String(res.invoice.amount || '');
				description = res.invoice.description || '';
				dueDate = res.invoice.due_date || '';
				mode = 'manual';
			}
		} catch (err) {
			error = err instanceof Error ? err.message : 'AI generation failed';
		} finally {
			aiLoading = false;
		}
	}

	async function handleSubmit(e: Event) {
		e.preventDefault();
		error = '';
		loading = true;
		try {
			await api('/payments/request', {
				method: 'POST',
				body: JSON.stringify({
					client_name: clientName,
					client_phone: clientPhone,
					client_email: clientEmail || null,
					amount: parsedAmount,
					description,
					due_date: dueDate,
					payment_method: paymentMethod
				})
			});
			goto('/payments');
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to create payment request';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Request Payment — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<!-- Back + Header -->
	<a href="/dashboard" class="mb-6 inline-flex items-center gap-1.5 text-[13px] text-white/25 transition-colors hover:text-white/50">
		<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
			<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
		</svg>
		Back to dashboard
	</a>
	<div class="mb-8">
		<p class="mb-1 text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Create</p>
		<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight text-white">
			Request <span class="italic text-emerald-400">Payment</span>
		</h1>
	</div>

	<div class="grid grid-cols-1 gap-6 lg:grid-cols-12">
		<!-- LEFT: Form -->
		<div class="lg:col-span-7">
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
				<div class="mb-4 rounded-xl border border-red-500/20 bg-red-500/[0.05] px-4 py-3 text-[13px] text-red-400">{error}</div>
			{/if}

			{#if mode === 'ai'}
				<div class="rounded-2xl border border-emerald-500/10 bg-emerald-500/[0.03] p-6 transition-all duration-500 delay-75 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<div class="mb-4 flex items-center gap-3">
						<div class="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-500/10">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
							</svg>
						</div>
						<div>
							<h3 class="text-[14px] font-semibold text-white/80">Describe the payment request</h3>
							<p class="text-[12px] text-white/20">e.g. "Request KES 12,000 from John Kamau for web design, due April 5"</p>
						</div>
					</div>
					<textarea
						bind:value={aiPrompt}
						rows={4}
						class="w-full rounded-xl border border-emerald-500/10 bg-white/[0.02] px-4 py-3 text-[13px] text-white placeholder-white/15 outline-none focus:border-emerald-500/30"
						placeholder="Describe the payment request in natural language..."
					></textarea>
					<button
						onclick={handleAIGenerate}
						disabled={aiLoading || !aiPrompt.trim()}
						class="mt-4 w-full rounded-xl bg-emerald-500 py-3 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400 disabled:opacity-40"
					>
						{#if aiLoading}
							<span class="inline-flex items-center gap-2">
								<svg class="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="3" stroke-dasharray="32" stroke-linecap="round" /></svg>
								Generating...
							</span>
						{:else}
							Generate Payment Request with AI
						{/if}
					</button>
				</div>
			{:else}
				<form onsubmit={handleSubmit} class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6 transition-all duration-500 delay-75 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<div class="space-y-5">
						<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
							<div>
								<label for="clientName" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Client Name</label>
								<input id="clientName" type="text" bind:value={clientName} required class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30" placeholder="John Kamau" />
							</div>
							<div>
								<label for="clientPhone" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Client Phone</label>
								<input id="clientPhone" type="tel" bind:value={clientPhone} required class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30" placeholder="0712345678" />
							</div>
						</div>
						<div>
							<label for="clientEmail" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Client Email <span class="normal-case tracking-normal text-white/15">(optional)</span></label>
							<input id="clientEmail" type="email" bind:value={clientEmail} class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30" placeholder="john@company.com" />
						</div>
						<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
							<div>
								<label for="amount" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Amount (KES)</label>
								<input id="amount" type="number" bind:value={amount} required min="1" class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30" placeholder="12000" />
							</div>
							<div>
								<label for="dueDate" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Due Date</label>
								<input id="dueDate" type="date" bind:value={dueDate} required class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30" />
							</div>
						</div>
						<div>
							<label for="paymentMethod" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Payment Method</label>
							<select id="paymentMethod" bind:value={paymentMethod} class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30">
								<option value="mpesa">M-Pesa STK Push</option>
								<option value="link">Payment Link</option>
								<option value="both">Both Options</option>
							</select>
						</div>
						<div>
							<label for="description" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Description</label>
							<textarea id="description" bind:value={description} required rows={3} class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30" placeholder="Web design services for company website"></textarea>
						</div>
					</div>
					<button
						type="submit"
						disabled={loading}
						class="mt-6 w-full rounded-xl bg-emerald-500 py-3 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400 disabled:opacity-40"
					>
						{loading ? 'Creating...' : 'Request Payment'}
					</button>
				</form>
			{/if}
		</div>

		<!-- RIGHT: Live Preview -->
		<div class="lg:col-span-5">
			<div class="sticky top-24 rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6 transition-all duration-500 delay-150 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-5 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Live Preview</span>
					<div class="flex h-6 w-6 items-center justify-center rounded-md bg-white/[0.03]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-white/20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
							<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
						</svg>
					</div>
				</div>

				{#if !hasPreviewData}
					<!-- Empty preview -->
					<div class="flex flex-col items-center py-12 text-center">
						<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-white/[0.03]">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white/15" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18.75a60.07 60.07 0 0115.79 4.101a6.067 6.067 0 014.101 4.101V10.5a6.067 6.067 0 00-4.101-4.101A60.07 60.07 0 002.25 6.75v12z" />
							</svg>
						</div>
						<p class="mt-4 text-[13px] text-white/20">Fill in the form to see a live preview</p>
					</div>
				{:else}
					<!-- Payment request preview card -->
					<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] p-5">
						<!-- Header -->
						<div class="flex items-start justify-between">
							<div>
								<p class="text-[10px] font-medium uppercase tracking-[0.15em] text-white/20">Payment Request</p>
								<p class="mt-1 text-[11px] text-white/15">Draft</p>
							</div>
							<img src="/logo-gold.png" alt="" class="h-6 w-6 opacity-40" />
						</div>

						<div class="my-4 border-t border-white/[0.04]"></div>

						<!-- Request from -->
						<div class="mb-4">
							<p class="text-[10px] font-medium uppercase tracking-[0.15em] text-white/20">Request From</p>
							<p class="mt-1.5 text-[14px] font-semibold text-white/80">{clientName || 'Client Name'}</p>
							{#if clientPhone}
								<p class="mt-0.5 text-[12px] text-white/25">{clientPhone}</p>
							{/if}
							{#if clientEmail}
								<p class="text-[12px] text-white/25">{clientEmail}</p>
							{/if}
						</div>

						<!-- Amount -->
						<div class="mb-4 rounded-lg bg-emerald-500/[0.06] px-4 py-3">
							<p class="text-[10px] font-medium uppercase tracking-[0.15em] text-emerald-500/60">Amount Requested</p>
							<p class="mt-1 font-['Instrument_Serif'] text-2xl italic text-emerald-400">
								{parsedAmount > 0 ? formatKES(parsedAmount) : 'KES 0'}
							</p>
						</div>

						<!-- Details -->
						<div class="space-y-3">
							{#if description}
								<div>
									<p class="text-[10px] font-medium uppercase tracking-[0.15em] text-white/20">Description</p>
									<p class="mt-1 text-[12px] leading-relaxed text-white/40">{description}</p>
								</div>
							{/if}
							{#if dueDate}
								<div>
									<p class="text-[10px] font-medium uppercase tracking-[0.15em] text-white/20">Due Date</p>
									<p class="mt-1 text-[12px] text-white/40">{new Date(dueDate + 'T00:00:00').toLocaleDateString('en-KE', { dateStyle: 'long' })}</p>
								</div>
							{/if}
							<div>
								<p class="text-[10px] font-medium uppercase tracking-[0.15em] text-white/20">Payment Method</p>
								<p class="mt-1 text-[12px] text-white/40">{paymentMethod === 'mpesa' ? 'M-Pesa STK Push' : paymentMethod === 'link' ? 'Payment Link' : 'M-Pesa + Payment Link'}</p>
							</div>
						</div>

						<div class="my-4 border-t border-white/[0.04]"></div>

						<!-- Footer -->
						<div class="flex items-center justify-between">
							<p class="text-[10px] text-white/15">Powered by CashFlow AI</p>
							<span class="rounded-full border border-white/[0.06] px-2 py-0.5 text-[10px] text-white/20">M-Pesa Ready</span>
						</div>
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>
