<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	interface Contact {
		id: string;
		name: string;
		phone: string;
		lastTransaction?: string;
		frequency?: string;
	}

	interface AIPrediction {
		recipient: Contact;
		amount: number;
		reason: string;
		confidence: number;
	}

	let loading = $state(true);
	let visible = $state(false);
	let mode = $state<'ai' | 'manual'>('ai');
	let selectedContact = $state<Contact | null>(null);
	let amount = $state('');
	let reason = $state('');
	let sending = $state(false);
	let searchQuery = $state('');

	// Mock contacts data
	let contacts = $state<Contact[]>([
		{ id: '1', name: 'Mary Wanjiku', phone: '0712345678', lastTransaction: '2 days ago', frequency: 'Weekly' },
		{ id: '2', name: 'John Kamau', phone: '0723456789', lastTransaction: '1 week ago', frequency: 'Monthly' },
		{ id: '3', name: 'Grace Njeri', phone: '0734567890', lastTransaction: '3 days ago', frequency: 'Weekly' },
		{ id: '4', name: 'David Mwangi', phone: '0745678901', lastTransaction: '2 weeks ago', frequency: 'Occasional' },
		{ id: '5', name: 'Samuel Ochieng', phone: '0756789012', lastTransaction: '5 days ago', frequency: 'Weekly' }
	]);

	// AI Predictions
	let aiPredictions = $state<AIPrediction[]>([
		{
			recipient: { id: '1', name: 'Mary Wanjiku', phone: '0712345678', frequency: 'Weekly' },
			amount: 5000,
			reason: 'Weekly supplier payment',
			confidence: 0.92
		},
		{
			recipient: { id: '2', name: 'John Kamau', phone: '0723456789', frequency: 'Monthly' },
			amount: 15000,
			reason: 'Monthly salary advance',
			confidence: 0.87
		}
	]);

	onMount(() => {
		if (!$auth.token) { goto('/login'); return; }
		setTimeout(() => (visible = true), 50);
		loading = false;
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
		// Auto-fill amount based on AI prediction
		const prediction = aiPredictions.find(p => p.recipient.id === contact.id);
		if (prediction && mode === 'ai') {
			amount = prediction.amount.toString();
			reason = prediction.reason;
		}
	}

	function getConfidenceColor(confidence: number) {
		if (confidence >= 0.9) return 'text-emerald-400';
		if (confidence >= 0.7) return 'text-amber-400';
		return 'text-red-400';
	}

	function getConfidenceText(confidence: number) {
		if (confidence >= 0.9) return 'High';
		if (confidence >= 0.7) return 'Medium';
		return 'Low';
	}
</script>

<svelte:head>
	<title>Send Money — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-4xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<!-- Header -->
	<div class="mb-8">
		<a href="/payments" class="mb-4 inline-flex items-center gap-2 text-[13px] text-white/40 transition-colors hover:text-white/60">
			<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
				<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
			</svg>
			Back to Payments
		</a>
		<p class="mb-1 text-[12px] font-medium uppercase tracking-[0.15em] text-white/25">Money Transfer</p>
		<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight text-white md:text-4xl">Send Money</h1>
		<p class="mt-2 text-[15px] text-white/40">AI-powered transfers and manual payments</p>
	</div>

	{#if loading}
		<!-- Skeleton -->
		<div class="animate-pulse">
			<div class="mb-6 h-12 w-full rounded-xl bg-white/[0.04]"></div>
			<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
				{#each Array(4) as _}
					<div class="h-24 rounded-xl bg-white/[0.02]"></div>
				{/each}
			</div>
		</div>
	{:else}
		<!-- Mode Toggle -->
		<div class="mb-8 flex gap-2 rounded-xl border border-white/[0.04] bg-white/[0.02] p-1">
			<button
				onclick={() => (mode = 'ai')}
				class="flex-1 rounded-lg px-4 py-3 text-[13px] font-medium transition-all {mode === 'ai' ? 'bg-emerald-500 text-zinc-950' : 'text-white/60'}"
			>
				<div class="flex items-center justify-center gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
					</svg>
					AI Assistant
				</div>
			</button>
			<button
				onclick={() => (mode = 'manual')}
				class="flex-1 rounded-lg px-4 py-3 text-[13px] font-medium transition-all {mode === 'manual' ? 'bg-emerald-500 text-zinc-950' : 'text-white/60'}"
			>
				<div class="flex items-center justify-center gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v12m6-6H6" />
					</svg>
					Manual Transfer
				</div>
			</button>
		</div>

		<div class="grid grid-cols-1 gap-8 lg:grid-cols-3">
			<!-- Left Column -->
			<div class="lg:col-span-2 space-y-6">
				{#if mode === 'ai'}
					<!-- AI Predictions -->
					<div class="rounded-2xl border border-emerald-500/10 bg-emerald-500/[0.03] p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
						<div class="mb-4 flex items-center gap-2">
							<div class="flex h-6 w-6 items-center justify-center rounded-full bg-emerald-400">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
									<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
								</svg>
							</div>
							<span class="text-[11px] font-medium text-emerald-400">AI Predictions</span>
						</div>
						<p class="mb-4 text-[13px] text-white/60">Based on your payment history and patterns</p>
						
						<div class="space-y-3">
							{#each aiPredictions as prediction}
								<button
									onclick={() => selectContact(prediction.recipient)}
									class="w-full rounded-xl border border-emerald-500/20 bg-emerald-500/[0.02] p-4 text-left transition-all hover:border-emerald-500/40 hover:bg-emerald-500/[0.05]"
								>
									<div class="flex items-center justify-between">
										<div class="flex items-center gap-3">
											<div class="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500/10">
												<span class="text-[10px] font-bold text-emerald-400">{prediction.recipient.name.charAt(0).toUpperCase()}</span>
											</div>
											<div>
												<p class="text-[13px] font-medium text-white/80">{prediction.recipient.name}</p>
												<p class="text-[11px] text-white/40">{prediction.reason}</p>
											</div>
										</div>
										<div class="text-right">
											<p class="text-lg font-medium text-emerald-400">{formatKES(prediction.amount)}</p>
											<div class="flex items-center gap-1">
												<span class="text-[10px] {getConfidenceColor(prediction.confidence)}">{getConfidenceText(prediction.confidence)}</span>
												<span class="text-[10px] text-white/20">({Math.round(prediction.confidence * 100)}%)</span>
											</div>
										</div>
									</div>
								</button>
							{/each}
						</div>
					</div>
				{/if}

				<!-- Contact Search -->
				<div class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">
						{mode === 'ai' ? 'Or Search Contacts' : 'Select Recipient'}
					</span>
					
					<div class="mb-4">
						<input
							type="text"
							bind:value={searchQuery}
							placeholder="Search by name or phone number..."
							class="w-full rounded-xl border border-white/[0.06] bg-white/[0.03] px-4 py-3 text-white placeholder-white/20 outline-none transition-colors focus:border-emerald-500/50 focus:bg-white/[0.05]"
						/>
					</div>

					<div class="space-y-2 max-h-64 overflow-y-auto">
						{#each filteredContacts as contact}
							<button
								onclick={() => selectContact(contact)}
								class="w-full rounded-xl border border-white/[0.04] bg-white/[0.01] p-3 text-left transition-all hover:border-white/[0.08] hover:bg-white/[0.05] {selectedContact?.id === contact.id ? 'border-emerald-500/50 bg-emerald-500/[0.05]' : ''}"
							>
								<div class="flex items-center justify-between">
									<div class="flex items-center gap-3">
										<div class="flex h-8 w-8 items-center justify-center rounded-full bg-white/[0.05]">
											<span class="text-[10px] font-medium text-white/60">{contact.name.charAt(0).toUpperCase()}</span>
										</div>
										<div>
											<p class="text-[13px] font-medium text-white/80">{contact.name}</p>
											<p class="text-[11px] text-white/40">{contact.phone}</p>
										</div>
									</div>
									<div class="text-right">
										{#if contact.frequency}
											<span class="text-[10px] text-white/30">{contact.frequency}</span>
										{/if}
									</div>
								</div>
							</button>
						{/each}
					</div>
				</div>
			</div>

			<!-- Right Column - Payment Details -->
			<div class="space-y-6">
				<!-- Payment Form -->
				<div class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Payment Details</span>
					
					{#if selectedContact}
						<div class="mb-4 rounded-xl border border-white/[0.04] bg-white/[0.01] p-3">
							<div class="flex items-center gap-3">
								<div class="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500/10">
									<span class="text-[10px] font-bold text-emerald-400">{selectedContact.name.charAt(0).toUpperCase()}</span>
								</div>
								<div>
									<p class="text-[13px] font-medium text-white/80">{selectedContact.name}</p>
									<p class="text-[11px] text-white/40">{selectedContact.phone}</p>
								</div>
							</div>
						</div>
					{:else}
						<div class="mb-4 rounded-xl border border-white/[0.04] bg-white/[0.01] p-3">
							<p class="text-center text-[13px] text-white/40">Select a recipient to continue</p>
						</div>
					{/if}

					<div class="space-y-4">
						<div>
							<label class="mb-2 block text-[11px] font-medium text-white/60">Amount (KES)</label>
							<input
								type="number"
								bind:value={amount}
								placeholder="0.00"
								min="0"
								step="100"
								disabled={!selectedContact}
								class="w-full rounded-xl border border-white/[0.06] bg-white/[0.03] px-4 py-3 text-white placeholder-white/20 outline-none transition-colors focus:border-emerald-500/50 focus:bg-white/[0.05] disabled:opacity-50"
							/>
						</div>

						{#if mode === 'manual'}
							<div>
								<label class="mb-2 block text-[11px] font-medium text-white/60">Reason (Optional)</label>
								<input
									type="text"
									bind:value={reason}
									placeholder="Payment description..."
									disabled={!selectedContact}
									class="w-full rounded-xl border border-white/[0.06] bg-white/[0.03] px-4 py-3 text-white placeholder-white/20 outline-none transition-colors focus:border-emerald-500/50 focus:bg-white/[0.05] disabled:opacity-50"
								/>
							</div>
						{:else if reason}
							<div>
								<label class="mb-2 block text-[11px] font-medium text-white/60">AI Suggested Reason</label>
								<div class="rounded-xl border border-emerald-500/20 bg-emerald-500/[0.02] px-4 py-3">
									<p class="text-[13px] text-emerald-400">{reason}</p>
								</div>
							</div>
						{/if}

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
				<div class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Quick Amounts</span>
					<div class="grid grid-cols-3 gap-2">
						{#each [1000, 2000, 5000, 10000, 15000, 20000] as quickAmount}
							<button
								onclick={() => (amount = quickAmount.toString())}
								disabled={!selectedContact}
								class="rounded-lg border border-white/[0.04] bg-white/[0.01] py-2 text-[12px] text-white/60 transition-all hover:border-white/[0.08] hover:bg-white/[0.05] disabled:opacity-50"
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
