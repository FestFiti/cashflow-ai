<script lang="ts">
	import { onMount } from 'svelte';
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { theme } from '$lib/stores/theme';
	import { showError, showSuccess } from '$lib/stores/toast';
	import { getAvatarUrl } from '$lib/avatar';

	const isDark = $derived($theme === 'dark');

	interface Invoice {
		id: string;
		business_id: string;
		client_name: string;
		client_phone: string;
		client_email: string;
		amount: number;
		description: string;
		due_date: string;
		status: 'draft' | 'sent' | 'paid' | 'overdue';
		payment_url: string | null;
		pdf_url: string | null;
		created_at: string;
		items: any[];
	}

	type StatusFilter = 'all' | 'draft' | 'sent' | 'overdue' | 'paid';
	type SortKey = 'created_at' | 'amount' | 'due_date';

	let invoices = $state<Invoice[]>([]);
	let loading = $state(true);
	let visible = $state(false);
	let searchQuery = $state('');
	let activeFilter = $state<StatusFilter>('all');
	let sortBy = $state<SortKey>('created_at');
	let sendingIds = $state<Set<string>>(new Set());

	const statusCounts = $derived({
		all: invoices.length,
		draft: invoices.filter((i) => i.status === 'draft').length,
		sent: invoices.filter((i) => i.status === 'sent').length,
		overdue: invoices.filter((i) => i.status === 'overdue').length,
		paid: invoices.filter((i) => i.status === 'paid').length
	});

	const filteredInvoices = $derived.by(() => {
		let result = invoices;

		// Status filter
		if (activeFilter !== 'all') {
			result = result.filter((i) => i.status === activeFilter);
		}

		// Search
		if (searchQuery.trim()) {
			const q = searchQuery.toLowerCase().trim();
			result = result.filter((i) => i.client_name.toLowerCase().includes(q));
		}

		// Sort
		result = [...result].sort((a, b) => {
			if (sortBy === 'amount') return b.amount - a.amount;
			if (sortBy === 'due_date') return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
			return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
		});

		return result;
	});

	const filteredTotal = $derived(filteredInvoices.reduce((sum, i) => sum + i.amount, 0));

	onMount(async () => {
		if (!$auth.token) {
			goto('/login');
			return;
		}
		try {
			invoices = await api<Invoice[]>('/invoices/', { token: $auth.token });
		} catch {
			invoices = [];
			showError('Failed to load invoices');
		} finally {
			loading = false;
			setTimeout(() => (visible = true), 50);
		}
	});

	function statusColor(status: string) {
		switch (status) {
			case 'paid':
				return 'border-emerald-500/20 bg-emerald-500/10 text-emerald-400';
			case 'sent':
				return 'border-blue-500/20 bg-blue-500/10 text-blue-400';
			case 'overdue':
				return 'border-red-500/20 bg-red-500/10 text-red-400';
			case 'draft':
				return `border-zinc-500/20 ${isDark ? 'bg-white/[0.04] text-white/40' : 'bg-zinc-100 text-zinc-500'}`;
			default:
				return `${isDark ? 'border-white/[0.08] bg-white/[0.03] text-white/40' : 'border-zinc-200 bg-white text-zinc-500'}`;
		}
	}

	function formatDueDate(date: string) {
		const d = new Date(date);
		const now = new Date();
		const diffDays = Math.ceil((d.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));

		const formatted = d.toLocaleDateString('en-KE', { month: 'short', day: 'numeric', year: 'numeric' });

		if (diffDays < 0) return { text: formatted, sub: `${Math.abs(diffDays)}d overdue`, urgent: true };
		if (diffDays === 0) return { text: formatted, sub: 'Due today', urgent: true };
		if (diffDays <= 3) return { text: formatted, sub: `Due in ${diffDays}d`, urgent: true };
		return { text: formatted, sub: '', urgent: false };
	}

	async function sendInvoice(e: Event, invoice: Invoice) {
		e.preventDefault();
		e.stopPropagation();

		if (sendingIds.has(invoice.id)) return;

		sendingIds = new Set([...sendingIds, invoice.id]);

		try {
			await api(`/invoices/${invoice.id}/send`, {
				method: 'POST',
				token: $auth.token!
			});
			// Update local status
			invoices = invoices.map((i) => (i.id === invoice.id ? { ...i, status: 'sent' as const } : i));
			showSuccess(`Invoice sent to ${invoice.client_name}`);
		} catch (err: any) {
			showError(err.message || 'Failed to send invoice');
		} finally {
			const next = new Set(sendingIds);
			next.delete(invoice.id);
			sendingIds = next;
		}
	}

	async function shareInvoice(e: Event, invoice: Invoice) {
		e.preventDefault();
		e.stopPropagation();

		const url = `${window.location.origin}/pay/${invoice.id}`;
		try {
			await navigator.clipboard.writeText(url);
			showSuccess('Payment link copied to clipboard');
		} catch {
			showError('Failed to copy link');
		}
	}

	const tabs: { key: StatusFilter; label: string }[] = [
		{ key: 'all', label: 'All' },
		{ key: 'draft', label: 'Draft' },
		{ key: 'sent', label: 'Sent' },
		{ key: 'overdue', label: 'Overdue' },
		{ key: 'paid', label: 'Paid' }
	];

	const sortOptions: { key: SortKey; label: string }[] = [
		{ key: 'created_at', label: 'Newest' },
		{ key: 'amount', label: 'Amount' },
		{ key: 'due_date', label: 'Due date' }
	];
</script>

<svelte:head>
	<title>Invoices — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link
		href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap"
		rel="stylesheet"
	/>
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<!-- Header -->
	<div class="mb-8 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
		<div>
			<p
				class="mb-1 text-[11px] font-medium uppercase tracking-[0.12em] {isDark
					? 'text-white/25'
					: 'text-zinc-400'}"
			>
				Billing
			</p>
			<h1
				class="font-['Instrument_Serif'] text-3xl tracking-tight {isDark
					? 'text-white'
					: 'text-zinc-900'} md:text-4xl"
			>
				<span class="italic text-emerald-400">Invoices</span>
			</h1>
		</div>
		<div class="flex items-center gap-2">
			<a
				href="/api/reports/export/invoices"
				target="_blank"
				class="inline-flex items-center gap-1.5 rounded-xl border px-4 py-2.5 text-[12px] font-medium transition-all {isDark ? 'border-white/[0.08] text-white/50 hover:border-white/20 hover:text-white' : 'border-zinc-200 text-zinc-500 hover:border-zinc-300 hover:text-zinc-700'}"
			>
				<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5M16.5 12L12 16.5m0 0L7.5 12m4.5 4.5V3"/></svg>
				Export
			</a>
			<a
				href="/invoices/new"
				class="group inline-flex items-center gap-2 rounded-xl bg-emerald-500 px-5 py-2.5 text-[13px] font-semibold text-zinc-950 shadow-lg shadow-emerald-500/20 transition-all hover:bg-emerald-400 hover:shadow-emerald-500/30"
			>
				<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
					<path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
				</svg>
				New Invoice
			</a>
		</div>
	</div>

	{#if loading}
		<!-- Skeleton -->
		<div class="space-y-4">
			<!-- Skeleton tabs -->
			<div class="flex gap-2">
				{#each Array(5) as _}
					<div
						class="h-9 w-20 animate-pulse rounded-lg {isDark
							? 'bg-white/[0.04]'
							: 'bg-zinc-100'}"
					></div>
				{/each}
			</div>
			<!-- Skeleton search bar -->
			<div
				class="h-11 w-full animate-pulse rounded-xl {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'}"
			></div>
			<!-- Skeleton rows -->
			{#each Array(5) as _}
				<div
					class="animate-pulse rounded-2xl border {isDark
						? 'border-white/[0.04]'
						: 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-5"
				>
					<div class="flex items-center justify-between">
						<div class="flex items-center gap-4">
							<div
								class="h-10 w-10 rounded-xl {isDark ? 'bg-white/[0.06]' : 'bg-zinc-100'}"
							></div>
							<div>
								<div
									class="mb-2 h-3.5 w-32 rounded {isDark
										? 'bg-white/[0.06]'
										: 'bg-zinc-100'}"
								></div>
								<div
									class="h-3 w-48 rounded {isDark ? 'bg-white/[0.06]' : 'bg-zinc-100'}"
								></div>
							</div>
						</div>
						<div class="flex items-center gap-3">
							<div
								class="h-8 w-20 rounded-lg {isDark ? 'bg-white/[0.06]' : 'bg-zinc-100'}"
							></div>
							<div
								class="h-8 w-16 rounded-lg {isDark ? 'bg-white/[0.06]' : 'bg-zinc-100'}"
							></div>
						</div>
					</div>
				</div>
			{/each}
		</div>
	{:else}
		<!-- Toolbar: Filter Tabs + Summary -->
		<div
			class="mb-4 transition-all duration-500 {visible
				? 'translate-y-0 opacity-100'
				: 'translate-y-3 opacity-0'}"
		>
			<!-- Status Tabs -->
			<div class="mb-4 flex flex-wrap gap-1.5">
				{#each tabs as tab}
					<button
						onclick={() => (activeFilter = tab.key)}
						class="inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-[12px] font-medium transition-all
							{activeFilter === tab.key
							? 'bg-emerald-500 text-zinc-950 shadow-sm shadow-emerald-500/20'
							: isDark
								? 'text-white/40 hover:bg-white/[0.04] hover:text-white/60'
								: 'text-zinc-500 hover:bg-zinc-100 hover:text-zinc-700'}"
					>
						{tab.label}
						<span
							class="ml-0.5 rounded-md px-1.5 py-0.5 text-[10px] font-semibold
								{activeFilter === tab.key
								? 'bg-emerald-600/30 text-zinc-950'
								: isDark
									? 'bg-white/[0.06] text-white/30'
									: 'bg-zinc-200/80 text-zinc-500'}"
						>
							{statusCounts[tab.key]}
						</span>
					</button>
				{/each}
			</div>

			<!-- Search + Sort + Total -->
			<div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
				<div class="flex flex-1 items-center gap-3">
					<!-- Search -->
					<div class="relative flex-1 max-w-md">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 {isDark
								? 'text-white/20'
								: 'text-zinc-400'}"
							fill="none"
							viewBox="0 0 24 24"
							stroke="currentColor"
							stroke-width="2"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z"
							/>
						</svg>
						<input
							type="text"
							placeholder="Search by client name..."
							bind:value={searchQuery}
							class="w-full rounded-xl border py-2.5 pl-10 pr-4 text-[13px] outline-none transition-all placeholder:{isDark
								? 'text-white/20'
								: 'text-zinc-400'} {isDark
								? 'border-white/[0.06] bg-white/[0.03] text-white/80 focus:border-emerald-500/40'
								: 'border-zinc-200 bg-white text-zinc-700 focus:border-emerald-500/60'}"
						/>
					</div>

					<!-- Sort -->
					<select
						bind:value={sortBy}
						class="rounded-xl border py-2.5 px-3 text-[12px] font-medium outline-none transition-all {isDark
							? 'border-white/[0.06] bg-white/[0.03] text-white/60'
							: 'border-zinc-200 bg-white text-zinc-600'}"
					>
						{#each sortOptions as opt}
							<option value={opt.key}>{opt.label}</option>
						{/each}
					</select>
				</div>

				<!-- Total -->
				<div class="flex items-center gap-2 text-right">
					<span class="text-[11px] font-medium uppercase tracking-[0.1em] {isDark ? 'text-white/25' : 'text-zinc-400'}">
						Total
					</span>
					<span class="text-[15px] font-semibold {isDark ? 'text-white' : 'text-zinc-900'}">
						{formatKES(filteredTotal)}
					</span>
				</div>
			</div>
		</div>

		{#if invoices.length === 0}
			<!-- Global empty state -->
			<div
				class="rounded-2xl border {isDark
					? 'border-white/[0.04]'
					: 'border-zinc-200'} {isDark
					? 'bg-white/[0.02]'
					: 'bg-white'} p-16 text-center transition-all duration-500 {visible
					? 'translate-y-0 opacity-100'
					: 'translate-y-3 opacity-0'}"
			>
				<div
					class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl {isDark
						? 'bg-white/[0.04]'
						: 'bg-zinc-50'}"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-7 w-7 {isDark ? 'text-white/15' : 'text-zinc-300'}"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="1.5"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z"
						/>
					</svg>
				</div>
				<h3
					class="mt-6 font-['Instrument_Serif'] text-xl {isDark
						? 'text-white'
						: 'text-zinc-900'}"
				>
					No invoices yet
				</h3>
				<p class="mt-2 text-[13px] {isDark ? 'text-white/25' : 'text-zinc-400'}">
					Create your first invoice to start tracking payments
				</p>
				<a
					href="/invoices/new"
					class="mt-6 inline-flex items-center gap-2 rounded-xl bg-emerald-500 px-6 py-2.5 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-4 w-4"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="2"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M12 4.5v15m7.5-7.5h-15"
						/>
					</svg>
					Create Invoice
				</a>
			</div>
		{:else if filteredInvoices.length === 0}
			<!-- Filter empty state -->
			<div
				class="rounded-2xl border {isDark
					? 'border-white/[0.04]'
					: 'border-zinc-200'} {isDark
					? 'bg-white/[0.02]'
					: 'bg-white'} p-12 text-center transition-all duration-300"
			>
				<div
					class="mx-auto flex h-14 w-14 items-center justify-center rounded-xl {isDark
						? 'bg-white/[0.04]'
						: 'bg-zinc-50'}"
				>
					<svg
						xmlns="http://www.w3.org/2000/svg"
						class="h-6 w-6 {isDark ? 'text-white/15' : 'text-zinc-300'}"
						fill="none"
						viewBox="0 0 24 24"
						stroke="currentColor"
						stroke-width="1.5"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M12 3c2.755 0 5.455.232 8.083.678.533.09.917.556.917 1.096v1.044a2.25 2.25 0 01-.659 1.591l-5.432 5.432a2.25 2.25 0 00-.659 1.591v2.927a2.25 2.25 0 01-1.244 2.013L9.75 21v-6.568a2.25 2.25 0 00-.659-1.591L3.659 7.409A2.25 2.25 0 013 5.818V4.774c0-.54.384-1.006.917-1.096A48.32 48.32 0 0112 3z"
						/>
					</svg>
				</div>
				<h3
					class="mt-5 font-['Instrument_Serif'] text-lg {isDark
						? 'text-white'
						: 'text-zinc-900'}"
				>
					{#if searchQuery.trim()}
						No invoices matching "{searchQuery}"
					{:else}
						No {activeFilter} invoices
					{/if}
				</h3>
				<p class="mt-1.5 text-[13px] {isDark ? 'text-white/25' : 'text-zinc-400'}">
					{#if searchQuery.trim()}
						Try a different search term
					{:else}
						Invoices with "{activeFilter}" status will appear here
					{/if}
				</p>
			</div>
		{:else}
			<!-- Invoice List -->
			<div
				class="overflow-hidden rounded-2xl border {isDark
					? 'border-white/[0.04]'
					: 'border-zinc-200'} {isDark
					? 'bg-white/[0.02]'
					: 'bg-white'} transition-all duration-500 {visible
					? 'translate-y-0 opacity-100'
					: 'translate-y-3 opacity-0'}"
			>
				<!-- Table Header (desktop) -->
				<div
					class="hidden border-b {isDark
						? 'border-white/[0.04]'
						: 'border-zinc-100'} px-5 py-3 md:grid md:grid-cols-12 md:gap-4"
				>
					<span
						class="col-span-4 text-[11px] font-medium uppercase tracking-[0.12em] {isDark
							? 'text-white/25'
							: 'text-zinc-400'}">Client</span
					>
					<span
						class="col-span-2 text-[11px] font-medium uppercase tracking-[0.12em] {isDark
							? 'text-white/25'
							: 'text-zinc-400'}">Amount</span
					>
					<span
						class="col-span-2 text-[11px] font-medium uppercase tracking-[0.12em] {isDark
							? 'text-white/25'
							: 'text-zinc-400'}">Due Date</span
					>
					<span
						class="col-span-1 text-[11px] font-medium uppercase tracking-[0.12em] {isDark
							? 'text-white/25'
							: 'text-zinc-400'}">Status</span
					>
					<span
						class="col-span-3 text-right text-[11px] font-medium uppercase tracking-[0.12em] {isDark
							? 'text-white/25'
							: 'text-zinc-400'}">Actions</span
					>
				</div>

				{#each filteredInvoices as invoice, i}
					{@const due = formatDueDate(invoice.due_date)}
					<div
						class="group flex flex-col gap-3 border-b last:border-b-0 {isDark
							? 'border-white/[0.04]'
							: 'border-zinc-100'} px-5 py-4 transition-all {isDark
							? 'hover:bg-white/[0.02]'
							: 'hover:bg-zinc-50/80'} md:grid md:grid-cols-12 md:items-center md:gap-4"
						style="transition-delay: {Math.min(i * 30, 300)}ms;"
					>
						<!-- Client -->
						<div class="col-span-4 flex items-center gap-3 min-w-0">
							<img
								src={getAvatarUrl(invoice.client_name)}
								alt={invoice.client_name}
								class="h-9 w-9 shrink-0 rounded-xl {isDark
									? 'ring-1 ring-white/[0.06]'
									: 'ring-1 ring-zinc-200/80'}"
							/>
							<div class="min-w-0">
								<p
									class="truncate text-[13px] font-medium {isDark
										? 'text-white/80'
										: 'text-zinc-700'}"
								>
									{invoice.client_name}
								</p>
								<p
									class="truncate text-[12px] {isDark
										? 'text-white/20'
										: 'text-zinc-400'}"
								>
									{invoice.description || invoice.client_email || 'No description'}
								</p>
							</div>
						</div>

						<!-- Amount -->
						<div class="col-span-2">
							<p
								class="text-[14px] font-semibold tabular-nums {isDark
									? 'text-white'
									: 'text-zinc-900'}"
							>
								{formatKES(invoice.amount)}
							</p>
						</div>

						<!-- Due Date -->
						<div class="col-span-2">
							<p
								class="text-[12px] {isDark ? 'text-white/40' : 'text-zinc-500'}"
							>
								{due.text}
							</p>
							{#if due.sub}
								<p
									class="text-[11px] font-medium {due.urgent
										? 'text-red-400'
										: isDark
											? 'text-white/20'
											: 'text-zinc-400'}"
								>
									{due.sub}
								</p>
							{/if}
						</div>

						<!-- Status -->
						<div class="col-span-1">
							<span
								class="inline-flex items-center rounded-full border px-2.5 py-0.5 text-[11px] font-medium capitalize {statusColor(
									invoice.status
								)}"
							>
								{invoice.status}
							</span>
						</div>

						<!-- Actions -->
						<div
							class="col-span-3 flex items-center justify-end gap-1.5"
						>
							<!-- View -->
							<a
								href="/invoices/{invoice.id}"
								class="inline-flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-[12px] font-medium transition-all {isDark
									? 'text-white/40 hover:bg-white/[0.06] hover:text-white/70'
									: 'text-zinc-500 hover:bg-zinc-100 hover:text-zinc-700'}"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="h-3.5 w-3.5"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
									stroke-width="2"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z"
									/>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
									/>
								</svg>
								View
							</a>

							<!-- Send (only for draft/sent) -->
							{#if invoice.status === 'draft' || invoice.status === 'sent'}
								<button
									onclick={(e) => sendInvoice(e, invoice)}
									disabled={sendingIds.has(invoice.id)}
									class="inline-flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-[12px] font-medium transition-all disabled:opacity-40
										{isDark
										? 'text-emerald-400/80 hover:bg-emerald-500/10 hover:text-emerald-400'
										: 'text-emerald-600 hover:bg-emerald-50 hover:text-emerald-700'}"
								>
									{#if sendingIds.has(invoice.id)}
										<svg
											class="h-3.5 w-3.5 animate-spin"
											xmlns="http://www.w3.org/2000/svg"
											fill="none"
											viewBox="0 0 24 24"
										>
											<circle
												class="opacity-25"
												cx="12"
												cy="12"
												r="10"
												stroke="currentColor"
												stroke-width="4"
											></circle>
											<path
												class="opacity-75"
												fill="currentColor"
												d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
											></path>
										</svg>
										Sending
									{:else}
										<svg
											xmlns="http://www.w3.org/2000/svg"
											class="h-3.5 w-3.5"
											fill="none"
											viewBox="0 0 24 24"
											stroke="currentColor"
											stroke-width="2"
										>
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												d="M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5"
											/>
										</svg>
										Send
									{/if}
								</button>
							{/if}

							<!-- Share -->
							<button
								onclick={(e) => shareInvoice(e, invoice)}
								class="inline-flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-[12px] font-medium transition-all {isDark
									? 'text-white/40 hover:bg-white/[0.06] hover:text-white/70'
									: 'text-zinc-500 hover:bg-zinc-100 hover:text-zinc-700'}"
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="h-3.5 w-3.5"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
									stroke-width="2"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m9.86-2.54a4.5 4.5 0 00-1.242-7.244l-4.5-4.5a4.5 4.5 0 00-6.364 6.364L4.343 8.28"
									/>
								</svg>
								Share
							</button>
						</div>
					</div>
				{/each}
			</div>

			<!-- Bottom count -->
			<p
				class="mt-3 text-center text-[12px] {isDark ? 'text-white/20' : 'text-zinc-400'}"
			>
				Showing {filteredInvoices.length} of {invoices.length} invoice{invoices.length !== 1
					? 's'
					: ''}
			</p>
		{/if}
	{/if}
</div>
