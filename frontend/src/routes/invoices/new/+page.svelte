<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { theme } from '$lib/stores/theme';
	import { showError, showSuccess } from '$lib/stores/toast';

	const isDark = $derived($theme === 'dark');

	// ---------- Types ----------
	interface Service {
		id: string;
		name: string;
		description: string;
		price: number;
		category: string;
		billing_type: string;
		billing_cycle: string | null;
		unit: string | null;
	}

	interface LineItem {
		id: string;
		service_id: string | null;
		name: string;
		description: string;
		quantity: number;
		unit_price: number;
	}

	// ---------- State ----------
	let mode = $state<'manual' | 'ai'>('ai');
	let aiPrompt = $state('');
	let aiLoading = $state(false);

	let clientName = $state('');
	let clientPhone = $state('');
	let clientEmail = $state('');
	let description = $state('');
	let dueDate = $state('');
	let loading = $state(false);
	let visible = $state(false);

	let services = $state<Service[]>([]);
	let items = $state<LineItem[]>([]);
	let showServicePicker = $state(false);
	let servicePickerEl = $state<HTMLDivElement | undefined>(undefined);

	// ---------- Derived ----------
	const total = $derived(items.reduce((sum, it) => sum + it.quantity * it.unit_price, 0));
	const hasPreviewData = $derived(clientName || total > 0 || description || items.length > 0);

	// ---------- Lifecycle ----------
	onMount(() => {
		if (!$auth.token) { goto('/login'); return; }
		setTimeout(() => (visible = true), 50);
		loadServices();
	});

	async function loadServices() {
		try {
			services = await api<Service[]>('/services/');
		} catch {
			// Services may not exist yet — that's fine
			services = [];
		}
	}

	// ---------- Helpers ----------
	function uid(): string {
		return crypto.randomUUID();
	}

	function addServiceItem(svc: Service) {
		items.push({
			id: uid(),
			service_id: svc.id,
			name: svc.name,
			description: svc.description || '',
			quantity: 1,
			unit_price: svc.price,
		});
		showServicePicker = false;
	}

	function addCustomItem() {
		items.push({
			id: uid(),
			service_id: null,
			name: '',
			description: '',
			quantity: 1,
			unit_price: 0,
		});
	}

	function removeItem(id: string) {
		items = items.filter(it => it.id !== id);
	}

	// Close service picker on outside click
	$effect(() => {
		if (showServicePicker) {
			const handler = (e: MouseEvent) => {
				if (servicePickerEl && !servicePickerEl.contains(e.target as Node)) {
					showServicePicker = false;
				}
			};
			document.addEventListener('click', handler, true);
			return () => document.removeEventListener('click', handler, true);
		}
	});

	// ---------- AI Generate ----------
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
				description = res.invoice.description || '';
				dueDate = res.invoice.due_date || '';

				// Try to match AI-generated description/amount to services as line items
				items = [];
				const aiAmount = Number(res.invoice.amount) || 0;
				let matched = false;

				if (services.length > 0 && description) {
					const descLower = description.toLowerCase();
					for (const svc of services) {
						if (descLower.includes(svc.name.toLowerCase())) {
							const qty = aiAmount > 0 && svc.price > 0 ? Math.max(1, Math.round(aiAmount / svc.price)) : 1;
							items.push({
								id: uid(),
								service_id: svc.id,
								name: svc.name,
								description: svc.description || '',
								quantity: qty,
								unit_price: svc.price,
							});
							matched = true;
						}
					}
				}

				// If no service matched but we have an amount, add a custom line item
				if (!matched && aiAmount > 0) {
					items.push({
						id: uid(),
						service_id: null,
						name: description || 'Service',
						description: '',
						quantity: 1,
						unit_price: aiAmount,
					});
				}

				mode = 'manual';
			}
		} catch (err) {
			showError(err instanceof Error ? err.message : 'AI generation failed');
		} finally {
			aiLoading = false;
		}
	}

	// ---------- Submit ----------
	async function handleSubmit(e: Event) {
		e.preventDefault();

		if (items.length === 0) {
			showError('Add at least one line item');
			return;
		}

		loading = true;
		try {
			const body: Record<string, any> = {
				client_name: clientName,
				client_phone: clientPhone,
				client_email: clientEmail || null,
				description,
				due_date: dueDate,
				items: items.map(it => ({
					service_id: it.service_id || null,
					name: it.name,
					description: it.description,
					quantity: it.quantity,
					unit_price: it.unit_price,
				})),
			};

			await api('/invoices/', {
				method: 'POST',
				body: JSON.stringify(body)
			});
			showSuccess('Invoice created');
			goto('/invoices');
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to create invoice');
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

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<!-- Back + Header -->
	<a href="/invoices" class="mb-6 inline-flex items-center gap-1.5 text-[13px] {isDark ? 'text-white/25' : 'text-zinc-400'} transition-colors {isDark ? 'hover:text-white/50' : 'hover:text-zinc-600'}">
		<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
			<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
		</svg>
		Back to invoices
	</a>
	<div class="mb-8">
		<p class="mb-1 text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Create</p>
		<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">
			New <span class="italic text-emerald-400">Invoice</span>
		</h1>
	</div>

	<div class="grid grid-cols-1 gap-6 lg:grid-cols-12">
		<!-- LEFT: Form -->
		<div class="lg:col-span-7">
			<!-- Mode Toggle -->
			<div class="mb-6 flex rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-1 transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
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
				<!-- AI Mode -->
				<div class="rounded-2xl border border-emerald-500/10 bg-emerald-500/[0.03] p-6 transition-all duration-500 delay-75 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<div class="mb-4 flex items-center gap-3">
						<div class="flex h-9 w-9 items-center justify-center rounded-lg bg-emerald-500/10">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
							</svg>
						</div>
						<div>
							<h3 class="text-[14px] font-semibold {isDark ? 'text-white/80' : 'text-zinc-700'}">Describe the invoice</h3>
							<p class="text-[12px] {isDark ? 'text-white/20' : 'text-zinc-400'}">e.g. "Invoice John Kamau KES 12,000 for web design, due April 5"</p>
						</div>
					</div>
					<textarea
						bind:value={aiPrompt}
						rows={4}
						class="w-full rounded-xl border border-emerald-500/10 {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-4 py-3 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} outline-none focus:border-emerald-500/30"
						placeholder="Describe the transaction in natural language..."
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
							Generate Invoice with AI
						{/if}
					</button>
				</div>
			{:else}
				<!-- Manual Mode -->
				<form onsubmit={handleSubmit} class="space-y-6 transition-all duration-500 delay-75 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<!-- Client Info Card -->
					<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
						<h3 class="mb-4 text-[13px] font-semibold uppercase tracking-[0.08em] {isDark ? 'text-white/40' : 'text-zinc-500'}">Client Information</h3>
						<div class="space-y-4">
							<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
								<div>
									<label for="clientName" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Client Name</label>
									<input id="clientName" type="text" bind:value={clientName} required class="w-full rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} focus:border-emerald-500/30" placeholder="John Kamau" />
								</div>
								<div>
									<label for="clientPhone" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Client Phone</label>
									<input id="clientPhone" type="tel" bind:value={clientPhone} required class="w-full rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} focus:border-emerald-500/30" placeholder="0712345678" />
								</div>
							</div>
							<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
								<div>
									<label for="clientEmail" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Client Email <span class="normal-case tracking-normal {isDark ? 'text-white/15' : 'text-zinc-400'}">(optional)</span></label>
									<input id="clientEmail" type="email" bind:value={clientEmail} class="w-full rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} focus:border-emerald-500/30" placeholder="john@company.com" />
								</div>
								<div>
									<label for="dueDate" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Due Date</label>
									<input id="dueDate" type="date" bind:value={dueDate} required class="w-full rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} focus:border-emerald-500/30" />
								</div>
							</div>
							<div>
								<label for="description" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Description</label>
								<textarea id="description" bind:value={description} rows={2} class="w-full rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} focus:border-emerald-500/30" placeholder="Web design services for company website"></textarea>
							</div>
						</div>
					</div>

					<!-- Line Items Card -->
					<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
						<div class="mb-4 flex items-center justify-between">
							<h3 class="text-[13px] font-semibold uppercase tracking-[0.08em] {isDark ? 'text-white/40' : 'text-zinc-500'}">Line Items</h3>
							<div class="flex items-center gap-2">
								{#if services.length > 0}
									<div class="relative" bind:this={servicePickerEl}>
										<button
											type="button"
											onclick={() => (showServicePicker = !showServicePicker)}
											class="inline-flex items-center gap-1.5 rounded-lg border {isDark ? 'border-emerald-500/20 bg-emerald-500/5 text-emerald-400' : 'border-emerald-200 bg-emerald-50 text-emerald-600'} px-3 py-1.5 text-[12px] font-medium transition-colors hover:bg-emerald-500/10"
										>
											<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
												<path stroke-linecap="round" stroke-linejoin="round" d="M13.5 16.875h3.375m0 0h3.375m-3.375 0V13.5m0 3.375v3.375M6 10.5h2.25a2.25 2.25 0 002.25-2.25V6a2.25 2.25 0 00-2.25-2.25H6A2.25 2.25 0 003.75 6v2.25A2.25 2.25 0 006 10.5zm0 9.75h2.25A2.25 2.25 0 0010.5 18v-2.25a2.25 2.25 0 00-2.25-2.25H6a2.25 2.25 0 00-2.25 2.25V18A2.25 2.25 0 006 20.25zm9.75-9.75H18a2.25 2.25 0 002.25-2.25V6A2.25 2.25 0 0018 3.75h-2.25A2.25 2.25 0 0013.5 6v2.25a2.25 2.25 0 002.25 2.25z" />
											</svg>
											Add from services
										</button>
										{#if showServicePicker}
											<div class="absolute right-0 z-50 mt-1.5 w-72 rounded-xl border shadow-lg {isDark ? 'border-white/[0.08] bg-zinc-900' : 'border-zinc-200 bg-white'} max-h-64 overflow-y-auto">
												{#each services as svc}
													<button
														type="button"
														onclick={() => addServiceItem(svc)}
														class="flex w-full items-center justify-between px-4 py-3 text-left transition-colors {isDark ? 'hover:bg-white/[0.04]' : 'hover:bg-zinc-50'} first:rounded-t-xl last:rounded-b-xl"
													>
														<div>
															<p class="text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">{svc.name}</p>
															{#if svc.category}
																<p class="text-[11px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{svc.category}</p>
															{/if}
														</div>
														<span class="text-[12px] font-medium text-emerald-500">{formatKES(svc.price)}</span>
													</button>
												{/each}
											</div>
										{/if}
									</div>
								{/if}
								<button
									type="button"
									onclick={addCustomItem}
									class="inline-flex items-center gap-1.5 rounded-lg border {isDark ? 'border-white/[0.08] text-white/50' : 'border-zinc-200 text-zinc-500'} px-3 py-1.5 text-[12px] font-medium transition-colors {isDark ? 'hover:border-white/[0.15] hover:text-white/70' : 'hover:border-zinc-300 hover:text-zinc-700'}"
								>
									<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
										<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
									</svg>
									Add custom item
								</button>
							</div>
						</div>

						{#if items.length === 0}
							<div class="flex flex-col items-center rounded-xl border border-dashed {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} py-10 text-center">
								<svg xmlns="http://www.w3.org/2000/svg" class="mb-3 h-8 w-8 {isDark ? 'text-white/10' : 'text-zinc-300'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1">
									<path stroke-linecap="round" stroke-linejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 002.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 00-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 00.75-.75 2.25 2.25 0 00-.1-.664m-5.8 0A2.251 2.251 0 0113.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25z" />
								</svg>
								<p class="text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'}">No items yet</p>
								<p class="mt-1 text-[11px] {isDark ? 'text-white/10' : 'text-zinc-300'}">Add from your services or create a custom item</p>
							</div>
						{:else}
							<div class="space-y-3">
								{#each items as item, i (item.id)}
									<div class="rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.01]' : 'border-zinc-100 bg-zinc-50/50'} p-4">
										<div class="mb-3 flex items-start justify-between">
											<span class="rounded-md {isDark ? 'bg-white/[0.04] text-white/20' : 'bg-zinc-100 text-zinc-400'} px-2 py-0.5 text-[10px] font-medium">
												{item.service_id ? 'SERVICE' : 'CUSTOM'} #{i + 1}
											</span>
											<button
												type="button"
												onclick={() => removeItem(item.id)}
												class="rounded-md p-1 transition-colors {isDark ? 'text-white/15 hover:bg-red-500/10 hover:text-red-400' : 'text-zinc-300 hover:bg-red-50 hover:text-red-500'}"
											>
												<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
													<path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
												</svg>
											</button>
										</div>
										<div class="grid grid-cols-1 gap-3 md:grid-cols-12">
											<div class="md:col-span-5">
												<label class="mb-1 block text-[10px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Name</label>
												<input type="text" bind:value={item.name} required class="w-full rounded-lg border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-3 py-2 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} focus:border-emerald-500/30" placeholder="Item name" />
											</div>
											<div class="md:col-span-3">
												<label class="mb-1 block text-[10px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Description</label>
												<input type="text" bind:value={item.description} class="w-full rounded-lg border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-3 py-2 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} focus:border-emerald-500/30" placeholder="Details" />
											</div>
											<div class="md:col-span-2">
												<label class="mb-1 block text-[10px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Qty</label>
												<input type="number" bind:value={item.quantity} min="1" required class="w-full rounded-lg border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-3 py-2 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none focus:border-emerald-500/30" />
											</div>
											<div class="md:col-span-2">
												<label class="mb-1 block text-[10px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Price</label>
												<input type="number" bind:value={item.unit_price} min="0" required class="w-full rounded-lg border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-3 py-2 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none focus:border-emerald-500/30" />
											</div>
										</div>
										<div class="mt-2 text-right">
											<span class="text-[12px] font-medium {isDark ? 'text-white/30' : 'text-zinc-400'}">
												Subtotal: <span class="text-emerald-500">{formatKES(item.quantity * item.unit_price)}</span>
											</span>
										</div>
									</div>
								{/each}
							</div>

							<!-- Total -->
							<div class="mt-4 flex items-center justify-between rounded-xl bg-emerald-500/[0.06] px-5 py-3.5">
								<span class="text-[12px] font-semibold uppercase tracking-[0.08em] text-emerald-500/70">Total</span>
								<span class="font-['Instrument_Serif'] text-xl italic text-emerald-400">{formatKES(total)}</span>
							</div>
						{/if}
					</div>

					<!-- Submit -->
					<button
						type="submit"
						disabled={loading || items.length === 0}
						class="w-full rounded-xl bg-emerald-500 py-3 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400 disabled:opacity-40"
					>
						{loading ? 'Creating...' : 'Create Invoice'}
					</button>
				</form>
			{/if}
		</div>

		<!-- RIGHT: Live Preview -->
		<div class="lg:col-span-5">
			<div class="sticky top-24 rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 transition-all duration-500 delay-150 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-5 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Live Preview</span>
					<div class="flex h-6 w-6 items-center justify-center rounded-md {isDark ? 'bg-white/[0.03]' : 'bg-white'}">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 {isDark ? 'text-white/20' : 'text-zinc-400'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
							<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
						</svg>
					</div>
				</div>

				{#if !hasPreviewData}
					<!-- Empty preview -->
					<div class="flex flex-col items-center py-12 text-center">
						<div class="flex h-12 w-12 items-center justify-center rounded-lg {isDark ? 'bg-white/[0.03]' : 'bg-white'}">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 {isDark ? 'text-white/15' : 'text-zinc-400'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
							</svg>
						</div>
						<p class="mt-4 text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Fill in the form to see a live preview</p>
					</div>
				{:else}
					<!-- Invoice preview card -->
					<div class="rounded-xl border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-5">
						<!-- Header -->
						<div class="flex items-start justify-between">
							<div>
								<p class="text-[10px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Invoice</p>
								<p class="mt-1 text-[11px] {isDark ? 'text-white/15' : 'text-zinc-400'}">Draft</p>
							</div>
							<img src="/logo-gold.png" alt="" class="h-6 w-6 opacity-40" />
						</div>

						<div class="my-4 border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-200'}"></div>

						<!-- Bill to -->
						<div class="mb-4">
							<p class="text-[10px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Bill To</p>
							<p class="mt-1.5 text-[14px] font-semibold {isDark ? 'text-white/80' : 'text-zinc-700'}">{clientName || 'Client Name'}</p>
							{#if clientPhone}
								<p class="mt-0.5 text-[12px] {isDark ? 'text-white/25' : 'text-zinc-400'}">{clientPhone}</p>
							{/if}
							{#if clientEmail}
								<p class="text-[12px] {isDark ? 'text-white/25' : 'text-zinc-400'}">{clientEmail}</p>
							{/if}
						</div>

						{#if dueDate}
							<div class="mb-4">
								<p class="text-[10px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Due Date</p>
								<p class="mt-1 text-[12px] {isDark ? 'text-white/40' : 'text-zinc-500'}">{new Date(dueDate + 'T00:00:00').toLocaleDateString('en-KE', { dateStyle: 'long' })}</p>
							</div>
						{/if}

						{#if description}
							<div class="mb-4">
								<p class="text-[10px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Description</p>
								<p class="mt-1 text-[12px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">{description}</p>
							</div>
						{/if}

						<!-- Line Items Table -->
						{#if items.length > 0}
							<div class="my-4 border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-200'}"></div>
							<p class="mb-2 text-[10px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Items</p>
							<div class="overflow-hidden rounded-lg border {isDark ? 'border-white/[0.04]' : 'border-zinc-100'}">
								<table class="w-full text-[11px]">
									<thead>
										<tr class="{isDark ? 'bg-white/[0.02]' : 'bg-zinc-50'}">
											<th class="px-3 py-2 text-left font-medium uppercase tracking-wider {isDark ? 'text-white/20' : 'text-zinc-400'}">Item</th>
											<th class="px-3 py-2 text-right font-medium uppercase tracking-wider {isDark ? 'text-white/20' : 'text-zinc-400'}">Qty</th>
											<th class="px-3 py-2 text-right font-medium uppercase tracking-wider {isDark ? 'text-white/20' : 'text-zinc-400'}">Price</th>
											<th class="px-3 py-2 text-right font-medium uppercase tracking-wider {isDark ? 'text-white/20' : 'text-zinc-400'}">Total</th>
										</tr>
									</thead>
									<tbody>
										{#each items as item (item.id)}
											<tr class="border-t {isDark ? 'border-white/[0.03]' : 'border-zinc-50'}">
												<td class="px-3 py-2 {isDark ? 'text-white/60' : 'text-zinc-600'}">
													{item.name || 'Untitled'}
													{#if item.description}
														<span class="{isDark ? 'text-white/20' : 'text-zinc-400'}"> - {item.description}</span>
													{/if}
												</td>
												<td class="px-3 py-2 text-right {isDark ? 'text-white/40' : 'text-zinc-500'}">{item.quantity}</td>
												<td class="px-3 py-2 text-right {isDark ? 'text-white/40' : 'text-zinc-500'}">{formatKES(item.unit_price)}</td>
												<td class="px-3 py-2 text-right font-medium {isDark ? 'text-white/60' : 'text-zinc-700'}">{formatKES(item.quantity * item.unit_price)}</td>
											</tr>
										{/each}
									</tbody>
								</table>
							</div>
						{/if}

						<!-- Amount -->
						<div class="mt-4 rounded-lg bg-emerald-500/[0.06] px-4 py-3">
							<p class="text-[10px] font-medium uppercase tracking-[0.15em] text-emerald-500/60">Amount Due</p>
							<p class="mt-1 font-['Instrument_Serif'] text-2xl italic text-emerald-400">
								{total > 0 ? formatKES(total) : 'KES 0'}
							</p>
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
