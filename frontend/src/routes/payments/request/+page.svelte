<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { theme } from '$lib/stores/theme';
	import { showError, showSuccess } from '$lib/stores/toast';
	import Select from '$lib/components/Select.svelte';

	const isDark = $derived($theme === 'dark');

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
			showError(err instanceof Error ? err.message : 'AI generation failed');
		} finally {
			aiLoading = false;
		}
	}

	async function handleSubmit(e: Event) {
		e.preventDefault();
		loading = true;
		try {
			// 1. Create invoice
			const invoice = await api<{ id: string }>('/invoices/', {
				method: 'POST',
				body: JSON.stringify({
					client_name: clientName,
					client_phone: clientPhone,
					client_email: clientEmail || null,
					amount: parsedAmount,
					description,
					due_date: dueDate,
				})
			});

			// 2. If M-Pesa, trigger STK push
			if (paymentMethod === 'mpesa' || paymentMethod === 'both') {
				try {
					await api('/payments/stk-push', {
						method: 'POST',
						body: JSON.stringify({ invoice_id: invoice.id, phone: clientPhone })
					});
					showSuccess('M-Pesa request sent! Check client phone.');
				} catch {
					showSuccess('Invoice created. STK push failed — send manually from invoice page.');
				}
			}

			// 3. If link/both, send invoice email
			if ((paymentMethod === 'link' || paymentMethod === 'both') && clientEmail) {
				try {
					await api(`/invoices/${invoice.id}/send`, { method: 'POST' });
				} catch { /* email send is best-effort */ }
			}

			goto(`/invoices/${invoice.id}`);
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to create payment request');
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
	<a href="/dashboard" class="mb-6 inline-flex items-center gap-1.5 text-[13px] {isDark ? 'text-white/25' : 'text-zinc-400'} transition-colors {isDark ? 'hover:text-white/50' : 'hover:text-zinc-600'}">
		<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
			<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
		</svg>
		Back to dashboard
	</a>
	<div class="mb-8">
		<p class="mb-1 text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Create</p>
		<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">
			Request <span class="italic text-emerald-400">Payment</span>
		</h1>
	</div>

	<div class="grid grid-cols-1 gap-6 lg:grid-cols-12">
		<!-- LEFT: Form -->
		<div class="lg:col-span-7">
			<!-- Mode Toggle -->
			<div class="mb-6 flex rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-1 transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
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
					class="flex flex-1 items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-[13px] font-medium transition-all {mode === 'manual' ? (isDark ? 'bg-zinc-800 text-white' : 'bg-zinc-100 text-zinc-900') : 'text-zinc-500'}"
				>
					<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
					</svg>
					Manual
				</button>
			</div>

			{#if mode === 'ai'}
				<div class="rounded-2xl border border-emerald-500/10 bg-emerald-500/[0.03] p-6 transition-all duration-500 delay-75 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<div class="mb-4 flex items-center gap-3">
						<div class="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-500/10">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
							</svg>
						</div>
						<div>
							<h3 class="text-[14px] font-semibold {isDark ? 'text-white/80' : 'text-zinc-700'}">Describe the payment request</h3>
							<p class="text-[12px] {isDark ? 'text-white/20' : 'text-zinc-400'}">e.g. "Request KES 12,000 from John Kamau for web design, due April 5"</p>
						</div>
					</div>
					<textarea
						bind:value={aiPrompt}
						rows={4}
						class="w-full rounded-xl border border-emerald-500/10 {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-4 py-3 text-[13px] {isDark ? 'text-white placeholder-white/15' : 'text-zinc-900 placeholder-zinc-400'} outline-none focus:border-emerald-500/30"
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
				<form onsubmit={handleSubmit} class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6 transition-all duration-500 delay-75 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<div class="space-y-5">
						<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
							<div>
								<label for="clientName" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Client Name</label>
								<input id="clientName" type="text" bind:value={clientName} required class="w-full rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} focus:border-emerald-500/30" placeholder="John Kamau" />
							</div>
							<div>
								<label for="clientPhone" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Client Phone</label>
								<input id="clientPhone" type="tel" bind:value={clientPhone} required class="w-full rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} focus:border-emerald-500/30" placeholder="0712345678" />
							</div>
						</div>
						<div>
							<label for="clientEmail" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Client Email <span class="normal-case tracking-normal {isDark ? 'text-white/15' : 'text-zinc-400'}">(optional)</span></label>
							<input id="clientEmail" type="email" bind:value={clientEmail} class="w-full rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} focus:border-emerald-500/30" placeholder="john@company.com" />
						</div>
						<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
							<div>
								<label for="amount" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Amount (KES)</label>
								<input id="amount" type="number" bind:value={amount} required min="1" class="w-full rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} focus:border-emerald-500/30" placeholder="12000" />
							</div>
							<div>
								<label for="dueDate" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Due Date</label>
								<input id="dueDate" type="date" bind:value={dueDate} required class="w-full rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} focus:border-emerald-500/30" />
							</div>
						</div>
						<div>
							<label for="paymentMethod" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Payment Method</label>
							<Select bind:value={paymentMethod} options={[
								{ value: 'mpesa', label: 'M-Pesa STK Push' },
								{ value: 'link', label: 'Payment Link' },
								{ value: 'both', label: 'Both Options' }
							]} />
						</div>
						<div>
							<label for="description" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Description</label>
							<textarea id="description" bind:value={description} required rows={3} class="w-full rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} focus:border-emerald-500/30" placeholder="Web design services for company website"></textarea>
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
			<div class="sticky top-24 rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6 transition-all duration-500 delay-150 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-5 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Live Preview</span>
					<div class="flex h-6 w-6 items-center justify-center rounded-md {isDark ? 'bg-white/[0.03]' : 'bg-zinc-50'}">
						<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 18 18" fill="none">
							<line x1="1.75" y1="7.25" x2="16.25" y2="7.25" stroke={isDark ? 'rgba(255,255,255,0.2)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
							<rect x="1.75" y="3.75" width="14.5" height="10.5" rx="2" ry="2" stroke={isDark ? 'rgba(255,255,255,0.2)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
							<line x1="4.25" y1="11.25" x2="7.25" y2="11.25" stroke={isDark ? 'rgba(255,255,255,0.2)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
							<line x1="12.75" y1="11.25" x2="13.75" y2="11.25" stroke={isDark ? 'rgba(255,255,255,0.2)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
						</svg>
					</div>
				</div>

				{#if !hasPreviewData}
					<!-- Empty preview -->
					<div class="flex flex-col items-center py-12 text-center">
						<div class="flex h-12 w-12 items-center justify-center rounded-lg {isDark ? 'bg-white/[0.03]' : 'bg-zinc-50'}">
							<svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 18 18" fill="none">
								<line x1="1.75" y1="7.25" x2="16.25" y2="7.25" stroke={isDark ? 'rgba(255,255,255,0.15)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								<rect x="1.75" y="3.75" width="14.5" height="10.5" rx="2" ry="2" stroke={isDark ? 'rgba(255,255,255,0.15)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								<line x1="4.25" y1="11.25" x2="7.25" y2="11.25" stroke={isDark ? 'rgba(255,255,255,0.15)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								<line x1="12.75" y1="11.25" x2="13.75" y2="11.25" stroke={isDark ? 'rgba(255,255,255,0.15)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</div>
						<p class="mt-4 text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Fill in the form to see a live preview</p>
					</div>
				{:else}
					<!-- Payment request preview card -->
					<div class="rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-5">
						<!-- Header -->
						<div class="flex items-start justify-between">
							<div>
								<p class="text-[10px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Payment Request</p>
								<p class="mt-1 text-[11px] {isDark ? 'text-white/15' : 'text-zinc-400'}">Draft</p>
							</div>
							<img src="/logo-gold.png" alt="" class="h-6 w-6 opacity-40" />
						</div>

						<div class="my-4 border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-200'}"></div>

						<!-- Request from -->
						<div class="mb-4">
							<p class="text-[10px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Request From</p>
							<p class="mt-1.5 text-[14px] font-semibold {isDark ? 'text-white/80' : 'text-zinc-700'}">{clientName || 'Client Name'}</p>
							{#if clientPhone}
								<p class="mt-0.5 text-[12px] {isDark ? 'text-white/25' : 'text-zinc-400'}">{clientPhone}</p>
							{/if}
							{#if clientEmail}
								<p class="text-[12px] {isDark ? 'text-white/25' : 'text-zinc-400'}">{clientEmail}</p>
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
									<p class="text-[10px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Description</p>
									<p class="mt-1 text-[12px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">{description}</p>
								</div>
							{/if}
							{#if dueDate}
								<div>
									<p class="text-[10px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Due Date</p>
									<p class="mt-1 text-[12px] {isDark ? 'text-white/40' : 'text-zinc-500'}">{new Date(dueDate + 'T00:00:00').toLocaleDateString('en-KE', { dateStyle: 'long' })}</p>
								</div>
							{/if}
							<div>
								<p class="text-[10px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Payment Method</p>
								<p class="mt-1 text-[12px] {isDark ? 'text-white/40' : 'text-zinc-500'}">{paymentMethod === 'mpesa' ? 'M-Pesa STK Push' : paymentMethod === 'link' ? 'Payment Link' : 'M-Pesa + Payment Link'}</p>
							</div>
						</div>

						<div class="my-4 border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-200'}"></div>

						<!-- Footer -->
						<div class="flex items-center justify-between">
							<p class="text-[10px] {isDark ? 'text-white/15' : 'text-zinc-400'}">Powered by CashFlow AI</p>
							<span class="rounded-full border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} px-2 py-0.5 text-[10px] {isDark ? 'text-white/20' : 'text-zinc-400'}">M-Pesa Ready</span>
						</div>
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>
