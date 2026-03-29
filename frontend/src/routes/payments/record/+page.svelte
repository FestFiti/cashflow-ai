<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let mode = $state<'manual' | 'confirm'>('manual');
	let payments = $state([]);
	let loading = $state(true);
	let error = $state('');
	let visible = $state(false);

	// Manual payment form
	let clientName = $state('');
	let clientPhone = $state('');
	let amount = $state('');
	let paymentMethod = $state('cash');
	let paymentDate = $state(new Date().toISOString().split('T')[0]);
	let reference = $state('');
	let notes = $state('');
	let submitting = $state(false);

	onMount(async () => {
		if (!$auth.token) { goto('/login'); return; }
		await loadPendingPayments();
		setTimeout(() => (visible = true), 50);
	});

	async function loadPendingPayments() {
		try {
			const res = await api<{ payments: any[] }>('/payments/pending');
			payments = res.payments || [];
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to load payments';
		} finally {
			loading = false;
		}
	}

	const parsedAmount = $derived(parseFloat(amount) || 0);

	async function handleManualRecord(e: Event) {
		e.preventDefault();
		if (!clientName || !amount) {
			error = 'Please fill all required fields';
			return;
		}

		submitting = true;
		error = '';
		try {
			await api('/payments/record', {
				method: 'POST',
				body: JSON.stringify({
					client_name: clientName,
					client_phone: clientPhone,
					amount: parsedAmount,
					payment_method: paymentMethod,
					payment_date: paymentDate,
					reference,
					notes
				})
			});
			
			// Reset form
			clientName = '';
			clientPhone = '';
			amount = '';
			reference = '';
			notes = '';
			paymentDate = new Date().toISOString().split('T')[0];
			
			// Reload pending payments
			await loadPendingPayments();
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to record payment';
		} finally {
			submitting = false;
		}
	}

	async function confirmPayment(paymentId: string) {
		try {
			await api(`/payments/${paymentId}/confirm`, {
				method: 'POST'
			});
			await loadPendingPayments();
		} catch (err) {
			error = err instanceof Error ? err.message : 'Failed to confirm payment';
		}
	}
</script>

<svelte:head>
	<title>Record Payment — CashFlow AI</title>
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
		<p class="mb-1 text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Manage</p>
		<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight text-white">
			Record <span class="italic text-emerald-400">Payment</span>
		</h1>
	</div>

	<!-- Mode Toggle -->
	<div class="mb-6 flex rounded-xl border border-white/[0.04] bg-white/[0.02] p-1 transition-all duration-500 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
		<button
			onclick={() => (mode = 'confirm')}
			class="flex flex-1 items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-[13px] font-medium transition-all {mode === 'confirm' ? 'bg-emerald-500 text-zinc-950' : 'text-zinc-500'}"
		>
			<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
				<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75l3 3m0 0l3-3m-3 3V7.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
			</svg>
			Confirm Expected
		</button>
		<button
			onclick={() => (mode = 'manual')}
			class="flex flex-1 items-center justify-center gap-2 rounded-lg px-4 py-2.5 text-[13px] font-medium transition-all {mode === 'manual' ? 'bg-zinc-800 text-white' : 'text-zinc-500'}"
		>
			<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
				<path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
			</svg>
			Manual Entry
		</button>
	</div>

	{#if error}
		<div class="mb-4 rounded-xl border border-red-500/20 bg-red-500/[0.05] px-4 py-3 text-[13px] text-red-400">{error}</div>
	{/if}

	{#if mode === 'confirm'}
		<!-- Confirm Expected Payments -->
		{#if loading}
			<div class="flex items-center justify-center py-12">
				<div class="h-8 w-8 animate-spin rounded-full border-2 border-emerald-500/30 border-t-emerald-500"></div>
			</div>
		{:else if payments.length === 0}
			<div class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-12 text-center">
				<div class="mx-auto mb-4 h-12 w-12 rounded-full bg-emerald-500/10 p-3">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M16.023 9.348h4.992v-.001M2.985 19.644v-4.992m0 0h4.992m-4.993 0l3.181 3.183a8.25 8.25 0 0013.803-3.7M4.031 9.865a8.25 8.25 0 0113.803-3.7l3.181 3.182m0-4.991v4.99" />
					</svg>
				</div>
				<h3 class="mb-2 text-lg font-medium text-white">No pending payments</h3>
				<p class="text-zinc-400">All payments have been confirmed.</p>
			</div>
		{:else}
			<div class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-6">
					<p class="text-[13px] text-white/60">Payments waiting for confirmation</p>
				</div>
				
				<div class="space-y-4">
					{#each payments as payment}
						<div class="rounded-xl border border-white/[0.04] bg-white/[0.02] p-5 transition-all hover:border-white/[0.08]">
							<div class="flex items-center justify-between">
								<div>
									<h3 class="text-[14px] font-semibold text-white/80">{payment.client_name}</h3>
									<p class="mt-1 text-[12px] text-white/40">{payment.description}</p>
									<p class="mt-2 text-[11px] text-white/20">Expected: {new Date(payment.due_date).toLocaleDateString()}</p>
								</div>
								<div class="text-right">
									<p class="text-lg font-medium text-white">{formatKES(payment.amount)}</p>
									<button
										onclick={() => confirmPayment(payment.id)}
										class="mt-2 rounded-xl bg-emerald-500 px-4 py-2 text-[11px] font-medium text-zinc-950 transition-colors hover:bg-emerald-400"
									>
										Confirm Payment
									</button>
								</div>
							</div>
						</div>
					{/each}
				</div>
			</div>
		{/if}
	{:else}
		<!-- Manual Payment Entry -->
		<form onsubmit={handleManualRecord} class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
			<div class="space-y-5">
				<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
					<div>
						<label for="clientName" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Client Name</label>
						<input id="clientName" type="text" bind:value={clientName} required class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30" placeholder="John Kamau" />
					</div>
					<div>
						<label for="clientPhone" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Client Phone</label>
						<input id="clientPhone" type="tel" bind:value={clientPhone} class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30" placeholder="0712345678" />
					</div>
				</div>

				<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
					<div>
						<label for="amount" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Amount (KES)</label>
						<input id="amount" type="number" bind:value={amount} required min="0" step="0.01" class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30" placeholder="5000" />
					</div>
					<div>
						<label for="paymentDate" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Payment Date</label>
						<input id="paymentDate" type="date" bind:value={paymentDate} class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30" />
					</div>
				</div>

				<div>
					<label for="paymentMethod" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Payment Method</label>
					<select id="paymentMethod" bind:value={paymentMethod} class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30">
						<option value="cash">Cash</option>
						<option value="bank">Bank Transfer</option>
						<option value="mpesa">M-Pesa</option>
						<option value="cheque">Cheque</option>
						<option value="other">Other</option>
					</select>
				</div>

				<div>
					<label for="reference" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Reference Number</label>
					<input id="reference" type="text" bind:value={reference} class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30" placeholder="Transaction ID, cheque number, etc." />
				</div>

				<div>
					<label for="notes" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Notes</label>
					<textarea id="notes" bind:value={notes} rows={3} class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30" placeholder="Additional details about this payment"></textarea>
				</div>
			</div>
			<button
				type="submit"
				disabled={submitting || !clientName || !amount}
				class="mt-6 w-full rounded-xl bg-emerald-500 py-3 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400 disabled:opacity-40"
			>
				{submitting ? 'Recording...' : 'Record Payment'}
			</button>
		</form>
	{/if}
</div>
