<script lang="ts">
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { theme } from '$lib/stores/theme';
	import { showError, showSuccess } from '$lib/stores/toast';

	const isDark = $derived($theme === 'dark');

	interface Service {
		id: string;
		name: string;
		description: string | null;
		price: number;
		created_at: string;
	}

	let services = $state<Service[]>([]);
	let loading = $state(true);
	let visible = $state(false);

	// Add form
	let showAddForm = $state(false);
	let addName = $state('');
	let addDescription = $state('');
	let addPrice = $state('');
	let addSaving = $state(false);

	// Edit state
	let editingId = $state<string | null>(null);
	let editName = $state('');
	let editDescription = $state('');
	let editPrice = $state('');
	let editSaving = $state(false);

	// Delete state
	let deletingId = $state<string | null>(null);
	let confirmDeleteId = $state<string | null>(null);

	// Selected service for detail panel
	let selectedService = $state<Service | null>(null);

	// Stats
	const totalValue = $derived(services.reduce((sum, s) => sum + s.price, 0));
	const avgPrice = $derived(services.length > 0 ? totalValue / services.length : 0);

	onMount(async () => {
		if (!$auth.token) { goto('/login'); return; }
		try {
			services = await api<Service[]>('/services/', { token: $auth.token });
		} catch {
			services = [];
		} finally {
			loading = false;
			setTimeout(() => (visible = true), 50);
		}
	});

	async function addService() {
		if (!addName.trim() || !addPrice.trim()) return;
		addSaving = true;
		try {
			const service = await api<Service>('/services/', {
				method: 'POST',
				body: JSON.stringify({
					name: addName.trim(),
					description: addDescription.trim() || null,
					price: parseFloat(addPrice)
				}),
				token: $auth.token!
			});
			services = [service, ...services];
			showSuccess('Service added');
			addName = '';
			addDescription = '';
			addPrice = '';
			showAddForm = false;
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to add service');
		} finally {
			addSaving = false;
		}
	}

	function startEdit(service: Service) {
		editingId = service.id;
		editName = service.name;
		editDescription = service.description || '';
		editPrice = service.price.toString();
	}

	function cancelEdit() {
		editingId = null;
	}

	async function saveEdit() {
		if (!editingId || !editName.trim() || !editPrice.trim()) return;
		editSaving = true;
		try {
			const updated = await api<Service>(`/services/${editingId}`, {
				method: 'PUT',
				body: JSON.stringify({
					name: editName.trim(),
					description: editDescription.trim() || null,
					price: parseFloat(editPrice)
				}),
				token: $auth.token!
			});
			services = services.map(s => s.id === editingId ? updated : s);
			showSuccess('Service updated');
			editingId = null;
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to update service');
		} finally {
			editSaving = false;
		}
	}

	async function deleteService(id: string) {
		deletingId = id;
		try {
			await api(`/services/${id}`, { method: 'DELETE', token: $auth.token! });
			services = services.filter(s => s.id !== id);
			showSuccess('Service deleted');
			confirmDeleteId = null;
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to delete service');
		} finally {
			deletingId = null;
		}
	}
</script>

<svelte:head>
	<title>Services — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<!-- Header -->
	<div class="mb-8 flex items-end justify-between">
		<div>
			<p class="mb-1 text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Catalog</p>
			<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'} md:text-4xl">
				<span class="italic text-emerald-400">Services</span>
			</h1>
		</div>
		<button
			onclick={() => { showAddForm = !showAddForm; }}
			class="group inline-flex items-center gap-2 rounded-xl bg-emerald-500 px-5 py-2.5 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400"
		>
			<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 transition-transform {showAddForm ? 'rotate-45' : ''}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
				<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
			</svg>
			{showAddForm ? 'Cancel' : 'Add Service'}
		</button>
	</div>

	<!-- Add Form -->
	{#if showAddForm}
		<div class="mb-6 rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 transition-all duration-300">
			<h3 class="mb-4 font-['Instrument_Serif'] text-xl {isDark ? 'text-white' : 'text-zinc-900'}">New Service</h3>
			<form onsubmit={(e) => { e.preventDefault(); addService(); }} class="grid gap-6 md:grid-cols-2">
				<div class="space-y-4">
					<div>
						<label class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Name *</label>
						<input
							bind:value={addName}
							type="text"
							required
							placeholder="e.g. Web Design"
							class="w-full rounded-xl border {isDark ? 'border-white/[0.08]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.03]' : 'bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} placeholder:{isDark ? 'text-white/20' : 'text-zinc-400'} focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500/20"
						/>
					</div>
					<div>
						<label class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Price (KES) *</label>
						<input
							bind:value={addPrice}
							type="number"
							required
							min="0"
							step="1"
							placeholder="5000"
							class="w-full rounded-xl border {isDark ? 'border-white/[0.08]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.03]' : 'bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} placeholder:{isDark ? 'text-white/20' : 'text-zinc-400'} focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500/20"
						/>
					</div>
				</div>
				<div class="flex flex-col space-y-4">
					<div class="flex-1">
						<label class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Description</label>
						<textarea
							bind:value={addDescription}
							rows="4"
							placeholder="Brief description of this service..."
							class="w-full h-[calc(100%-24px)] rounded-xl border {isDark ? 'border-white/[0.08]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.03]' : 'bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} placeholder:{isDark ? 'text-white/20' : 'text-zinc-400'} focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500/20 resize-none"
						></textarea>
					</div>
					<div class="flex justify-end">
						<button
							type="submit"
							disabled={addSaving || !addName.trim() || !addPrice.trim()}
							class="inline-flex items-center gap-2 rounded-xl bg-emerald-500 px-6 py-2.5 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400 disabled:cursor-not-allowed disabled:opacity-50"
						>
							{#if addSaving}
								<div class="h-4 w-4 animate-spin rounded-full border-2 border-zinc-950/30 border-t-zinc-950"></div>
								Saving...
							{:else}
								Save Service
							{/if}
						</button>
					</div>
				</div>
			</form>
		</div>
	{/if}

	<div class="grid grid-cols-1 gap-6 lg:grid-cols-12">
		<!-- LEFT: Services List -->
		<div class="lg:col-span-8">
			{#if loading}
				<div class="grid gap-4 md:grid-cols-2">
					{#each Array(4) as _}
						<div class="animate-pulse rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
							<div class="h-4 w-32 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
							<div class="mt-3 h-3 w-48 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
							<div class="mt-4 h-6 w-24 rounded {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"></div>
						</div>
					{/each}
				</div>
			{:else if services.length === 0}
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-12 text-center transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<div class="mx-auto flex h-14 w-14 items-center justify-center rounded-lg {isDark ? 'bg-white/[0.03]' : 'bg-zinc-50'}">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 {isDark ? 'text-white/20' : 'text-zinc-400'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M20.25 14.15v4.25c0 1.094-.787 2.036-1.872 2.18-2.087.277-4.216.42-6.378.42s-4.291-.143-6.378-.42c-1.085-.144-1.872-1.086-1.872-2.18v-4.25m16.5 0a2.18 2.18 0 00.75-1.661V8.706c0-1.081-.768-2.015-1.837-2.175a48.114 48.114 0 00-3.413-.387m4.5 8.006c-.194.165-.42.295-.673.38A23.978 23.978 0 0112 15.75c-2.648 0-5.195-.429-7.577-1.22a2.016 2.016 0 01-.673-.38m0 0A2.18 2.18 0 013 12.489V8.706c0-1.081.768-2.015 1.837-2.175a48.111 48.111 0 013.413-.387m7.5 0V5.25A2.25 2.25 0 0013.5 3h-3a2.25 2.25 0 00-2.25 2.25v.894m7.5 0a48.667 48.667 0 00-7.5 0M12 12.75h.008v.008H12v-.008z" />
						</svg>
					</div>
					<h3 class="mt-5 font-['Instrument_Serif'] text-xl {isDark ? 'text-white' : 'text-zinc-900'}">No services yet</h3>
					<p class="mt-2 text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Add your first service to use in invoices.</p>
					<button
						onclick={() => { showAddForm = true; }}
						class="mt-6 inline-flex items-center gap-2 rounded-xl bg-emerald-500 px-6 py-2.5 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400"
					>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
						</svg>
						Add Service
					</button>
				</div>
			{:else}
				<div class="grid gap-4 md:grid-cols-2 transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					{#each services as service, i}
						<button
							type="button"
							onclick={() => { selectedService = service; }}
							class="rounded-2xl border text-left {selectedService?.id === service.id ? (isDark ? 'border-emerald-500/30 bg-emerald-500/[0.04]' : 'border-emerald-500/30 bg-emerald-50/50') : (isDark ? 'border-white/[0.04]' : 'border-zinc-200')} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 transition-all {isDark ? 'hover:border-white/[0.08]' : 'hover:border-zinc-300'}"
							style="transition-delay: {i * 40}ms;"
						>
							{#if editingId === service.id}
								<!-- svelte-ignore a11y_click_events_have_key_events -->
								<form onsubmit={(e) => { e.preventDefault(); saveEdit(); }} onclick={(e) => e.stopPropagation()} class="space-y-3">
									<div>
										<label class="mb-1 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Name</label>
										<input
											bind:value={editName}
											type="text"
											required
											class="w-full rounded-lg border {isDark ? 'border-white/[0.08]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.03]' : 'bg-white'} px-3 py-2 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500/20"
										/>
									</div>
									<div>
										<label class="mb-1 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Description</label>
										<textarea
											bind:value={editDescription}
											rows="2"
											class="w-full rounded-lg border {isDark ? 'border-white/[0.08]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.03]' : 'bg-white'} px-3 py-2 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500/20 resize-none"
										></textarea>
									</div>
									<div>
										<label class="mb-1 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Price (KES)</label>
										<input
											bind:value={editPrice}
											type="number"
											required
											min="0"
											step="1"
											class="w-full rounded-lg border {isDark ? 'border-white/[0.08]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.03]' : 'bg-white'} px-3 py-2 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} focus:border-emerald-500 focus:outline-none focus:ring-1 focus:ring-emerald-500/20"
										/>
									</div>
									<div class="flex gap-2 pt-1">
										<button
											type="submit"
											disabled={editSaving}
											class="flex-1 rounded-lg bg-emerald-500 py-2 text-[12px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400 disabled:opacity-50"
										>
											{editSaving ? 'Saving...' : 'Save'}
										</button>
										<button
											type="button"
											onclick={cancelEdit}
											class="flex-1 rounded-lg border {isDark ? 'border-white/[0.08]' : 'border-zinc-200'} py-2 text-[12px] font-medium {isDark ? 'text-white/40' : 'text-zinc-500'} transition-all {isDark ? 'hover:border-white/[0.15]' : 'hover:border-zinc-300'}"
										>
											Cancel
										</button>
									</div>
								</form>
							{:else}
								<div class="flex items-start justify-between">
									<div class="min-w-0 flex-1">
										<h3 class="truncate text-[14px] font-semibold {isDark ? 'text-white/80' : 'text-zinc-700'}">{service.name}</h3>
										{#if service.description}
											<p class="mt-1 text-[12px] leading-relaxed {isDark ? 'text-white/25' : 'text-zinc-400'} line-clamp-2">{service.description}</p>
										{/if}
									</div>
								</div>
								<div class="mt-4 border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-100'} pt-4">
									<p class="font-['Instrument_Serif'] text-xl italic tracking-tight text-emerald-400">{formatKES(service.price)}</p>
								</div>
							{/if}
						</button>
					{/each}
				</div>
			{/if}
		</div>

		<!-- RIGHT: Detail Sidebar -->
		<div class="lg:col-span-4 space-y-4">
			<div class="sticky top-24 space-y-4">
				<!-- Catalog Summary -->
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 transition-all duration-500 delay-100 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Catalog Summary</span>
					<div class="space-y-4">
						<div>
							<p class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Total Services</p>
							<p class="mt-1 font-['Instrument_Serif'] text-3xl italic tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">{services.length}</p>
						</div>
						<div class="border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-100'} pt-4">
							<p class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Catalog Value</p>
							<p class="mt-1 font-['Instrument_Serif'] text-2xl italic tracking-tight text-emerald-400">{formatKES(totalValue)}</p>
						</div>
						<div class="border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-100'} pt-4">
							<p class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Average Price</p>
							<p class="mt-1 text-lg font-semibold {isDark ? 'text-white/60' : 'text-zinc-600'}">{formatKES(avgPrice)}</p>
						</div>
					</div>
				</div>

				<!-- Selected Service Detail -->
				{#if selectedService}
					<div class="rounded-2xl border {isDark ? 'border-emerald-500/10' : 'border-emerald-100'} {isDark ? 'bg-emerald-500/[0.03]' : 'bg-emerald-50/30'} p-6 transition-all duration-300">
						<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] text-emerald-500/70">Service Detail</span>
						<h3 class="font-['Instrument_Serif'] text-2xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">{selectedService.name}</h3>
						{#if selectedService.description}
							<p class="mt-2 text-[13px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">{selectedService.description}</p>
						{:else}
							<p class="mt-2 text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'} italic">No description</p>
						{/if}

						<div class="my-4 border-t {isDark ? 'border-white/[0.04]' : 'border-emerald-100'}"></div>

						<div class="space-y-3">
							<div>
								<p class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Price</p>
								<p class="mt-1 font-['Instrument_Serif'] text-3xl italic tracking-tight text-emerald-400">{formatKES(selectedService.price)}</p>
							</div>
							<div>
								<p class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Created</p>
								<p class="mt-1 text-[13px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">{new Date(selectedService.created_at).toLocaleDateString()}</p>
							</div>
						</div>

						<div class="mt-5 flex gap-2">
							<button
								onclick={() => startEdit(selectedService)}
								class="flex flex-1 items-center justify-center gap-2 rounded-xl bg-emerald-500 py-2.5 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400"
							>
								<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931z" />
								</svg>
								Edit
							</button>
							{#if confirmDeleteId === selectedService.id}
								<button
									onclick={() => { deleteService(selectedService.id); selectedService = null; }}
									disabled={deletingId === selectedService.id}
									class="flex flex-1 items-center justify-center gap-2 rounded-xl bg-red-500/10 py-2.5 text-[13px] font-semibold text-red-400 border border-red-500/20 transition-all hover:bg-red-500/20 disabled:opacity-50"
								>
									{deletingId === selectedService.id ? 'Deleting...' : 'Confirm Delete'}
								</button>
							{:else}
								<button
									onclick={() => { confirmDeleteId = selectedService.id; }}
									class="flex items-center justify-center gap-2 rounded-xl border {isDark ? 'border-white/[0.08]' : 'border-zinc-200'} px-4 py-2.5 text-[13px] font-medium {isDark ? 'text-white/40 hover:text-red-400 hover:border-red-500/20' : 'text-zinc-500 hover:text-red-500 hover:border-red-200'} transition-all"
								>
									<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
										<path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
									</svg>
								</button>
							{/if}
						</div>
					</div>
				{:else}
					<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 text-center transition-all duration-500 delay-200 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
						<div class="mx-auto flex h-10 w-10 items-center justify-center rounded-lg {isDark ? 'bg-white/[0.03]' : 'bg-zinc-50'}">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {isDark ? 'text-white/15' : 'text-zinc-300'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M15.042 21.672L13.684 16.6m0 0l-2.51 2.225.569-9.47 5.227 7.917-3.286-.672zM12 2.25V4.5m5.834.166l-1.591 1.591M20.25 10.5H18M7.757 14.743l-1.59 1.59M6 10.5H3.75m4.007-4.243l-1.59-1.59" />
							</svg>
						</div>
						<p class="mt-3 text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Select a service to view details</p>
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>
