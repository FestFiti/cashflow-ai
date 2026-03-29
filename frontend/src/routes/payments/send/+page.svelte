<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { theme } from '$lib/stores/theme';
	import { getAvatarUrl } from '$lib/avatar';

	const isDark = $derived($theme === 'dark');

	interface Contact {
		id: string;
		name: string;
		phone: string;
	}

	let loading = $state(true);
	let visible = $state(false);
	let mode = $state<'manual' | 'ai'>('manual');
	let selectedContact = $state<Contact | null>(null);
	let amount = $state('');
	let reason = $state('');
	let sending = $state(false);
	let searchQuery = $state('');
	let contacts = $state<Contact[]>([]);

	onMount(async () => {
		if (!$auth.token) { goto('/login'); return; }
		try {
			// Derive contacts from invoice clients
			const invoices = await api<{ id: string; client_name: string; client_phone: string }[]>('/invoices/');
			const seen = new Set<string>();
			contacts = invoices
				.filter(inv => { if (seen.has(inv.client_phone)) return false; seen.add(inv.client_phone); return true; })
				.map(inv => ({ id: inv.id, name: inv.client_name, phone: inv.client_phone }));
		} catch { /* empty is fine */ }
		loading = false;
		setTimeout(() => (visible = true), 50);
	});

	const filteredContacts = $derived(contacts.filter(contact =>
		contact.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
		contact.phone.includes(searchQuery)
	));

	async function handleSendMoney() {
		if (!selectedContact || !amount) return;

		sending = true;
		try {
			// TODO: Implement actual payment logic
			await new Promise(resolve => setTimeout(resolve, 2000));
			goto('/payments?success=true');
		} catch (error) {
			console.error('Payment failed:', error);
		} finally {
			sending = false;
		}
	}

	function selectContact(contact: Contact) {
		selectedContact = contact;
	}
</script>

<svelte:head>
	<title>Send Money — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<!-- Header -->
	<div class="mb-8">
		<a href="/payments" class="mb-4 inline-flex items-center gap-2 text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'} transition-colors {isDark ? 'hover:text-white/60' : 'hover:text-zinc-700'}">
			<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
				<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
			</svg>
			Back to Payments
		</a>
		<p class="mb-1 text-[12px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Money Transfer</p>
		<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'} md:text-4xl">Send Money</h1>
		<p class="mt-2 text-[15px] {isDark ? 'text-white/40' : 'text-zinc-500'}">AI-powered transfers and manual payments</p>
	</div>

	{#if loading}
		<!-- Skeleton -->
		<div class="animate-pulse">
			<div class="mb-6 h-12 w-full rounded-xl {isDark ? 'bg-white/[0.04]' : 'bg-zinc-200'}"></div>
			<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
				{#each Array(4) as _}
					<div class="h-24 rounded-xl {isDark ? 'bg-white/[0.02]' : 'bg-white'}"></div>
				{/each}
			</div>
		</div>
	{:else}
		<div class="grid grid-cols-1 gap-8 lg:grid-cols-3">
			<!-- Left Column -->
			<div class="lg:col-span-2 space-y-6">
				<!-- Contact Search -->
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">
						Select Recipient
					</span>

					<div class="mb-4">
						<input
							type="text"
							bind:value={searchQuery}
							placeholder="Search by name or phone number..."
							class="w-full rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.03]' : 'border-zinc-200 bg-white'} px-4 py-3 {isDark ? 'text-white placeholder-white/20' : 'text-zinc-900 placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-white'}"
						/>
					</div>

					<div class="space-y-2 max-h-64 overflow-y-auto">
						{#each filteredContacts as contact}
							<button
								onclick={() => selectContact(contact)}
								class="w-full rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.01]' : 'border-zinc-200 bg-white'} p-3 text-left transition-all {isDark ? 'hover:border-white/[0.08] hover:bg-white/[0.05]' : 'hover:border-zinc-300 hover:bg-zinc-50'} {selectedContact?.id === contact.id ? 'border-emerald-500/50 bg-emerald-500/[0.05]' : ''}"
							>
								<div class="flex items-center justify-between">
									<div class="flex items-center gap-3">
										<img src={getAvatarUrl(contact.name)} alt={contact.name} class="h-8 w-8 rounded-full" />
										<div>
											<p class="text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">{contact.name}</p>
											<p class="text-[11px] {isDark ? 'text-white/40' : 'text-zinc-500'}">{contact.phone}</p>
										</div>
									</div>
									<div class="text-right"></div>
								</div>
							</button>
						{/each}
					</div>
				</div>
			</div>

			<!-- Right Column - Payment Details -->
			<div class="space-y-6">
				<!-- Payment Form -->
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Payment Details</span>

					{#if selectedContact}
						<div class="mb-4 rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.01]' : 'border-zinc-200 bg-white'} p-3">
							<div class="flex items-center gap-3">
								<img src={getAvatarUrl(selectedContact.name)} alt={selectedContact.name} class="h-10 w-10 rounded-full" />
								<div>
									<p class="text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">{selectedContact.name}</p>
									<p class="text-[11px] {isDark ? 'text-white/40' : 'text-zinc-500'}">{selectedContact.phone}</p>
								</div>
							</div>
						</div>
					{:else}
						<div class="mb-4 rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.01]' : 'border-zinc-200 bg-white'} p-3">
							<p class="text-center text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'}">Select a recipient to continue</p>
						</div>
					{/if}

					<div class="space-y-4">
						<div>
							<label class="mb-2 block text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">Amount (KES)</label>
							<input
								type="number"
								bind:value={amount}
								placeholder="0.00"
								min="0"
								step="100"
								disabled={!selectedContact}
								class="w-full rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.03]' : 'border-zinc-200 bg-white'} px-4 py-3 {isDark ? 'text-white placeholder-white/20' : 'text-zinc-900 placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-white'} disabled:opacity-50"
							/>
						</div>

						<div>
							<label class="mb-2 block text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">Reason (Optional)</label>
							<input
								type="text"
								bind:value={reason}
								placeholder="Payment description..."
								disabled={!selectedContact}
								class="w-full rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.03]' : 'border-zinc-200 bg-white'} px-4 py-3 {isDark ? 'text-white placeholder-white/20' : 'text-zinc-900 placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-white'} disabled:opacity-50"
							/>
						</div>

						<button
							onclick={handleSendMoney}
							disabled={!selectedContact || !amount || sending}
							class="w-full rounded-xl bg-emerald-500 py-3 text-[13px] font-semibold text-zinc-950 transition-colors hover:bg-emerald-600 disabled:opacity-50"
						>
							{#if sending}
								<div class="flex items-center justify-center gap-2">
									<div class="h-4 w-4 animate-spin rounded-full border-2 border-zinc-950 border-t-transparent"></div>
									Sending...
								</div>
							{:else}
								Send {amount ? formatKES(Number(amount)) : 'Money'}
							{/if}
						</button>
					</div>
				</div>

				<!-- Quick Amounts -->
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Quick Amounts</span>
					<div class="grid grid-cols-3 gap-2">
						{#each [1000, 2000, 5000, 10000, 15000, 20000] as quickAmount}
							<button
								onclick={() => (amount = quickAmount.toString())}
								disabled={!selectedContact}
								class="rounded-lg border {isDark ? 'border-white/[0.04] bg-white/[0.01]' : 'border-zinc-200 bg-white'} py-2 text-[12px] {isDark ? 'text-white/60' : 'text-zinc-600'} transition-all {isDark ? 'hover:border-white/[0.08] hover:bg-white/[0.05]' : 'hover:border-zinc-300 hover:bg-zinc-50'} disabled:opacity-50"
							>
								{formatKES(quickAmount)}
							</button>
						{/each}
					</div>
				</div>
			</div>
		</div>
	{/if}
</div>
