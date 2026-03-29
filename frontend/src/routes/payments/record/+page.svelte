<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { theme } from '$lib/stores/theme';
	import { getAvatarUrl } from '$lib/avatar';
	import { showError } from '$lib/stores/toast';

	const isDark = $derived($theme === 'dark');

	let mode = $state<'manual' | 'confirm'>('manual');
	let payments = $state([]);
	let loading = $state(true);
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
			showError(err instanceof Error ? err.message : 'Failed to load payments');
		} finally {
			loading = false;
		}
	}

	const parsedAmount = $derived(parseFloat(amount) || 0);

	async function handleManualRecord(e: Event) {
		e.preventDefault();
		if (!clientName || !amount) {
			showError('Please fill all required fields');
			return;
		}

		submitting = true;
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

			clientName = '';
			clientPhone = '';
			amount = '';
			reference = '';
			notes = '';
			paymentDate = new Date().toISOString().split('T')[0];

			await loadPendingPayments();
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to record payment');
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
			showError(err instanceof Error ? err.message : 'Failed to confirm payment');
		}
	}

	function getMethodIcon(method: string) {
		switch (method) {
			case 'mpesa': return 'M';
			case 'bank': return 'B';
			case 'cheque': return 'C';
			case 'cash': return 'K';
			default: return 'O';
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
	<!-- Header -->
	<div class="mb-8">
		<a href="/payments" class="mb-4 inline-flex items-center gap-2 text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'} transition-colors {isDark ? 'hover:text-white/60' : 'hover:text-zinc-700'}">
			<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
				<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
			</svg>
			Back to Payments
		</a>
		<p class="mb-1 text-[12px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Payment Management</p>
		<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'} md:text-4xl">Record Payment</h1>
		<p class="mt-2 text-[15px] {isDark ? 'text-white/40' : 'text-zinc-500'}">Log incoming payments and confirm expected transactions</p>
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
		<!-- Mode Toggle -->
		<div class="mb-8 flex gap-2 rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-1">
			<button
				onclick={() => (mode = 'manual')}
				class="flex-1 rounded-lg px-4 py-3 text-[13px] font-medium transition-all {mode === 'manual' ? 'bg-emerald-500 text-zinc-950' : (isDark ? 'text-white/60' : 'text-zinc-600')}"
			>
				<div class="flex items-center justify-center gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
					</svg>
					Manual Entry
				</div>
			</button>
			<button
				onclick={() => (mode = 'confirm')}
				class="flex-1 rounded-lg px-4 py-3 text-[13px] font-medium transition-all {mode === 'confirm' ? 'bg-emerald-500 text-zinc-950' : (isDark ? 'text-white/60' : 'text-zinc-600')}"
			>
				<div class="flex items-center justify-center gap-2">
					<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
						<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
					</svg>
					Confirm Expected
				</div>
			</button>
		</div>

		<div class="grid grid-cols-1 gap-8 lg:grid-cols-3">
			<!-- Left Column -->
			<div class="lg:col-span-2 space-y-6">
				{#if mode === 'manual'}
					<!-- Manual Entry Form -->
					<form onsubmit={handleManualRecord} class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
						<span class="mb-5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Client Information</span>

						<div class="space-y-4">
							<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
								<div>
									<label for="clientName" class="mb-2 block text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">Client Name *</label>
									<input
										id="clientName"
										type="text"
										bind:value={clientName}
										required
										placeholder="John Kamau"
										class="w-full rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.03]' : 'border-zinc-200 bg-white'} px-4 py-3 text-[14px] {isDark ? 'text-white placeholder-white/20' : 'text-zinc-900 placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-white'}"
									/>
								</div>
								<div>
									<label for="clientPhone" class="mb-2 block text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">Phone Number</label>
									<input
										id="clientPhone"
										type="tel"
										bind:value={clientPhone}
										placeholder="0712345678"
										class="w-full rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.03]' : 'border-zinc-200 bg-white'} px-4 py-3 text-[14px] {isDark ? 'text-white placeholder-white/20' : 'text-zinc-900 placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-white'}"
									/>
								</div>
							</div>

							<div class="my-5 border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-200'}"></div>
							<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Payment Information</span>

							<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
								<div>
									<label for="amount" class="mb-2 block text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">Amount (KES) *</label>
									<input
										id="amount"
										type="number"
										bind:value={amount}
										required
										min="0"
										step="0.01"
										placeholder="0.00"
										class="w-full rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.03]' : 'border-zinc-200 bg-white'} px-4 py-3 text-[14px] {isDark ? 'text-white placeholder-white/20' : 'text-zinc-900 placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-white'}"
									/>
								</div>
								<div>
									<label for="paymentDate" class="mb-2 block text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">Payment Date</label>
									<input
										id="paymentDate"
										type="date"
										bind:value={paymentDate}
										class="w-full rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.03]' : 'border-zinc-200 bg-white'} px-4 py-3 text-[14px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-white'}"
									/>
								</div>
							</div>

							<div>
								<label for="paymentMethod" class="mb-2 block text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">Payment Method</label>
								<div class="grid grid-cols-2 gap-2 md:grid-cols-5">
									{#each [
										{ value: 'cash', label: 'Cash', icon: '💵' },
										{ value: 'mpesa', label: 'M-Pesa', icon: '📱' },
										{ value: 'bank', label: 'Bank', icon: '🏦' },
										{ value: 'cheque', label: 'Cheque', icon: '📝' },
										{ value: 'other', label: 'Other', icon: '💳' }
									] as method}
										<button
											type="button"
											onclick={() => (paymentMethod = method.value)}
											class="rounded-xl border px-3 py-2.5 text-[12px] font-medium transition-all {paymentMethod === method.value ? 'border-emerald-500/50 bg-emerald-500/[0.05] text-emerald-400' : (isDark ? 'border-white/[0.04] bg-white/[0.01] text-white/60 hover:border-white/[0.08] hover:bg-white/[0.05]' : 'border-zinc-200 bg-white text-zinc-600 hover:border-zinc-300 hover:bg-zinc-50')}"
										>
											{method.icon} {method.label}
										</button>
									{/each}
								</div>
							</div>

							<div>
								<label for="reference" class="mb-2 block text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">Reference Number</label>
								<input
									id="reference"
									type="text"
									bind:value={reference}
									placeholder="Transaction ID, cheque number, etc."
									class="w-full rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.03]' : 'border-zinc-200 bg-white'} px-4 py-3 text-[14px] {isDark ? 'text-white placeholder-white/20' : 'text-zinc-900 placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-white'}"
								/>
							</div>

							<div>
								<label for="notes" class="mb-2 block text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">Notes (Optional)</label>
								<textarea
									id="notes"
									bind:value={notes}
									rows={3}
									placeholder="Additional details about this payment..."
									class="w-full rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.03]' : 'border-zinc-200 bg-white'} px-4 py-3 text-[14px] {isDark ? 'text-white placeholder-white/20' : 'text-zinc-900 placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-white'}"
								></textarea>
							</div>
						</div>

						<button
							type="submit"
							disabled={submitting || !clientName || !amount}
							class="mt-6 w-full rounded-xl bg-emerald-500 py-3 text-[13px] font-semibold text-zinc-950 transition-colors hover:bg-emerald-600 disabled:opacity-50"
						>
							{#if submitting}
								<div class="flex items-center justify-center gap-2">
									<div class="h-4 w-4 animate-spin rounded-full border-2 border-zinc-950 border-t-transparent"></div>
									Recording...
								</div>
							{:else}
								Record {parsedAmount > 0 ? formatKES(parsedAmount) : 'Payment'}
							{/if}
						</button>
					</form>
				{:else}
					<!-- Confirm Expected Payments -->
					{#if payments.length === 0}
						<div class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-12 text-center transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
							<div class="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-full bg-emerald-500/10">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
									<path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
								</svg>
							</div>
							<h3 class="mb-2 text-lg font-medium {isDark ? 'text-white' : 'text-zinc-900'}">No pending payments</h3>
							<p class="text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'}">All expected payments have been confirmed.</p>
						</div>
					{:else}
						<div class="space-y-3 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
							{#each payments as payment}
								<div class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-5 transition-all {isDark ? 'hover:border-white/[0.08]' : 'hover:border-zinc-300'}">
									<div class="flex items-center justify-between">
										<div class="flex items-center gap-3">
											<img src={getAvatarUrl(payment.client_name || 'payment')} alt={payment.client_name} class="h-10 w-10 rounded-full" />
											<div>
												<p class="text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">{payment.client_name}</p>
												<p class="text-[11px] {isDark ? 'text-white/40' : 'text-zinc-500'}">{payment.description}</p>
												<p class="mt-1 text-[10px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Expected: {new Date(payment.due_date).toLocaleDateString()}</p>
											</div>
										</div>
										<div class="text-right">
											<p class="text-lg font-medium text-emerald-400">{formatKES(payment.amount)}</p>
											<button
												onclick={() => confirmPayment(payment.id)}
												class="mt-2 rounded-lg bg-emerald-500 px-4 py-2 text-[11px] font-medium text-zinc-950 transition-colors hover:bg-emerald-600"
											>
												Confirm
											</button>
										</div>
									</div>
								</div>
							{/each}
						</div>
					{/if}
				{/if}
			</div>

			<!-- Right Column - Summary -->
			<div class="space-y-6">
				<!-- Payment Preview -->
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Payment Preview</span>

					{#if clientName || parsedAmount > 0}
						<div class="space-y-3">
							<div class="flex items-center gap-3">
								<img src={getAvatarUrl(clientName || 'client')} alt="Client" class="h-10 w-10 rounded-full" />
								<div>
									<p class="text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">{clientName || 'Client name'}</p>
									<p class="text-[11px] {isDark ? 'text-white/40' : 'text-zinc-500'}">{clientPhone || 'No phone'}</p>
								</div>
							</div>

							<div class="border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} pt-3">
								<p class="text-2xl font-medium text-emerald-400">{parsedAmount > 0 ? formatKES(parsedAmount) : 'KES 0.00'}</p>
							</div>

							<div class="space-y-2 border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} pt-3">
								<div class="flex justify-between">
									<span class="text-[11px] {isDark ? 'text-white/40' : 'text-zinc-500'}">Method</span>
									<span class="text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">{paymentMethod.charAt(0).toUpperCase() + paymentMethod.slice(1)}</span>
								</div>
								<div class="flex justify-between">
									<span class="text-[11px] {isDark ? 'text-white/40' : 'text-zinc-500'}">Date</span>
									<span class="text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">{new Date(paymentDate).toLocaleDateString()}</span>
								</div>
								{#if reference}
									<div class="flex justify-between">
										<span class="text-[11px] {isDark ? 'text-white/40' : 'text-zinc-500'}">Reference</span>
										<span class="text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">{reference}</span>
									</div>
								{/if}
							</div>
						</div>
					{:else}
						<div class="py-6 text-center">
							<div class="mx-auto mb-3 flex h-10 w-10 items-center justify-center rounded-full {isDark ? 'bg-white/[0.03]' : 'bg-zinc-100'}">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 {isDark ? 'text-white/20' : 'text-zinc-400'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
									<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
								</svg>
							</div>
							<p class="text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'}">Fill in the form to preview</p>
						</div>
					{/if}
				</div>

				<!-- Quick Amounts -->
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
					<span class="mb-4 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Quick Amounts</span>
					<div class="grid grid-cols-3 gap-2">
						{#each [1000, 2000, 5000, 10000, 15000, 20000] as quickAmount}
							<button
								type="button"
								onclick={() => (amount = quickAmount.toString())}
								class="rounded-lg border {isDark ? 'border-white/[0.04] bg-white/[0.01]' : 'border-zinc-200 bg-white'} py-2 text-[12px] {isDark ? 'text-white/60' : 'text-zinc-600'} transition-all {isDark ? 'hover:border-white/[0.08] hover:bg-white/[0.05]' : 'hover:border-zinc-300 hover:bg-zinc-50'}"
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
