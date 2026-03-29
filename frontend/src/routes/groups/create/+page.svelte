<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { theme } from '$lib/stores/theme';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { showError } from '$lib/stores/toast';
	import Select from '$lib/components/Select.svelte';

	const isDark = $derived($theme === 'dark');
	let groupName = $state('');
	let groupDescription = $state('');
	let contributionAmount = $state('');
	let contributionFrequency = $state('monthly');
	let contributionDay = $state('1');
	const dayOptions = $derived(
		contributionFrequency === 'monthly'
			? Array.from({ length: 31 }, (_, i) => ({ value: String(i + 1), label: `${i + 1}${i === 0 ? 'st' : i === 1 ? 'nd' : i === 2 ? 'rd' : 'th'}` }))
			: contributionFrequency === 'weekly'
				? [{ value: '1', label: 'Monday' }, { value: '2', label: 'Tuesday' }, { value: '3', label: 'Wednesday' }, { value: '4', label: 'Thursday' }, { value: '5', label: 'Friday' }, { value: '6', label: 'Saturday' }, { value: '7', label: 'Sunday' }]
				: [{ value: '1', label: '1st Period' }, { value: '2', label: '2nd Period' }, { value: '3', label: '3rd Period' }, { value: '4', label: '4th Period' }]
	);
	let members = $state([{ name: '', phone: '', email: '' }]);
	let loading = $state(false);
	let visible = $state(false);

	onMount(() => {
		if (!$auth.token) { goto('/login'); return; }
		setTimeout(() => (visible = true), 50);
	});

	const parsedAmount = $derived(parseFloat(contributionAmount) || 0);

	function addMember() {
		members = [...members, { name: '', phone: '', email: '' }];
	}

	function removeMember(index: number) {
		if (members.length > 1) {
			members = members.filter((_, i) => i !== index);
		}
	}

	function updateMember(index: number, field: string, value: string) {
		members[index] = { ...members[index], [field]: value };
		members = [...members];
	}

	async function handleCreateGroup(e: Event) {
		e.preventDefault();
		if (!groupName || !contributionAmount || members.some(m => !m.name || !m.phone)) {
			showError('Please fill all required fields');
			return;
		}

		loading = true;
		try {
			const res = await api<{ status: string; group: any }>('/groups/create', {
				method: 'POST',
				body: JSON.stringify({
					name: groupName,
					description: groupDescription,
					contribution_amount: parsedAmount,
					contribution_frequency: contributionFrequency,
					contribution_day: parseInt(contributionDay),
					members: members.filter(m => m.name || m.phone || m.email)
				})
			});

			// Redirect to group dashboard
			goto(`/groups/${res.group.id}`);
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to create group');
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Create Group — CashFlow AI</title>
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
			Create <span class="italic text-emerald-400">Group</span>
		</h1>
	</div>

	<div class="grid grid-cols-1 gap-6 lg:grid-cols-12">
		<!-- LEFT: Form -->
		<div class="lg:col-span-7">
			<form onsubmit={handleCreateGroup} class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="space-y-5">
					<!-- Group Information -->
					<div>
						<label for="groupName" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Group Name</label>
						<input id="groupName" type="text" bind:value={groupName} required class="w-full rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} focus:border-emerald-500/30" placeholder="e.g., Office Chama, Investment Club" />
					</div>

					<div>
						<label for="groupDescription" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Description</label>
						<textarea id="groupDescription" bind:value={groupDescription} rows={3} class="w-full rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} focus:border-emerald-500/30" placeholder="What is this group for? What are the goals?"></textarea>
					</div>

					<!-- Contribution Settings -->
					<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
						<div>
							<label for="contributionAmount" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Contribution Amount (KES)</label>
							<input id="contributionAmount" type="number" bind:value={contributionAmount} required min="0" step="0.01" class="w-full rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-4 py-2.5 text-[13px] {isDark ? 'text-white' : 'text-zinc-900'} outline-none {isDark ? 'placeholder-white/15' : 'placeholder-zinc-400'} focus:border-emerald-500/30" placeholder="5000" />
						</div>
						<div>
							<label for="contributionFrequency" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Frequency</label>
							<Select bind:value={contributionFrequency} options={[
								{ value: 'daily', label: 'Daily' },
								{ value: 'weekly', label: 'Weekly' },
								{ value: 'monthly', label: 'Monthly' },
								{ value: 'quarterly', label: 'Quarterly' }
							]} />
						</div>
					</div>

					<div>
						<label for="contributionDay" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">
							{contributionFrequency === 'monthly' ? 'Day of Month' : contributionFrequency === 'weekly' ? 'Day of Week' : 'Time Period'}
						</label>
						<Select bind:value={contributionDay} options={dayOptions} />
					</div>

					<!-- Members -->
					<div>
						<div class="mb-4 flex items-center justify-between">
							<label class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Group Members</label>
							<button
								type="button"
								onclick={addMember}
								class="rounded-lg border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} px-3 py-1 text-[11px] font-medium {isDark ? 'text-white' : 'text-zinc-900'} transition-colors {isDark ? 'hover:bg-white/[0.05]' : 'hover:bg-zinc-50'}"
							>
								+ Add Member
							</button>
						</div>

						<div class="space-y-3">
							{#each members as member, index}
								<div class="rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.01]' : 'bg-white'} p-4">
									<div class="grid grid-cols-3 gap-3">
										<div>
											<input
												type="text"
												bind:value={member.name}
												placeholder="Full Name *"
												class="w-full rounded-lg border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-3 py-2 text-sm {isDark ? 'text-white' : 'text-zinc-900'} {isDark ? 'placeholder-white/20' : 'placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-zinc-50'}"
												required
											/>
										</div>
										<div>
											<input
												type="tel"
												bind:value={member.phone}
												placeholder="Phone *"
												class="w-full rounded-lg border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-3 py-2 text-sm {isDark ? 'text-white' : 'text-zinc-900'} {isDark ? 'placeholder-white/20' : 'placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-zinc-50'}"
												required
											/>
										</div>
										<div class="flex gap-2">
											<input
												type="email"
												bind:value={member.email}
												placeholder="Email (optional)"
												class="flex-1 rounded-lg border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-3 py-2 text-sm {isDark ? 'text-white' : 'text-zinc-900'} {isDark ? 'placeholder-white/20' : 'placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-zinc-50'}"
											/>
											{#if members.length > 1}
												<button
													type="button"
													onclick={() => removeMember(index)}
													class="rounded-lg border border-red-500/20 bg-red-500/10 px-2 py-1 text-red-400 transition-colors hover:bg-red-500/20"
												>
													<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
														<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
													</svg>
												</button>
											{/if}
										</div>
									</div>
								</div>
							{/each}
						</div>
					</div>
				</div>

				<button
					type="submit"
					disabled={loading || !groupName || !contributionAmount || members.some(m => !m.name || !m.phone)}
					class="mt-6 w-full rounded-xl bg-emerald-500 py-3 text-[13px] font-semibold text-zinc-950 transition-all hover:bg-emerald-400 disabled:opacity-40"
				>
					{loading ? 'Creating...' : 'Create Group'}
				</button>
			</form>
		</div>

		<!-- RIGHT: Preview -->
		<div class="lg:col-span-5">
			<div class="sticky top-24 rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6 transition-all duration-500 delay-150 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-5 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Group Preview</span>
						<div class="flex h-6 w-6 items-center justify-center rounded-md {isDark ? 'bg-white/[0.03]' : 'bg-white'}">
							<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 18 18" fill="none">
								<path d="M6.5 8.25C7.743 8.25 8.75 7.243 8.75 6C8.75 4.757 7.743 3.75 6.5 3.75C5.257 3.75 4.25 4.757 4.25 6C4.25 7.243 5.257 8.25 6.5 8.25Z" stroke={isDark ? 'rgba(255,255,255,0.2)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								<path d="M1.75 14.25C1.75 11.767 3.878 9.75 6.5 9.75C7.28 9.75 8.017 9.934 8.667 10.261" stroke={isDark ? 'rgba(255,255,255,0.2)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								<path d="M13.25 16.25C15.045 16.25 16.5 14.795 16.25 13C16.25 11.205 14.795 9.75 13 9.75C11.205 9.75 9.75 11.205 9.75 13C9.75 14.795 11.205 16.25 13 16.25" stroke={isDark ? 'rgba(255,255,255,0.2)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								<line x1="13" y1="11.25" x2="13" y2="14.75" stroke={isDark ? 'rgba(255,255,255,0.2)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								<line x1="11.25" y1="13" x2="14.75" y2="13" stroke={isDark ? 'rgba(255,255,255,0.2)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</div>
				</div>

				{#if !groupName}
					<!-- Empty preview -->
					<div class="flex flex-col items-center py-12 text-center">
							<div class="flex h-12 w-12 items-center justify-center rounded-lg {isDark ? 'bg-white/[0.03]' : 'bg-zinc-50'}">
								<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 18 18" fill="none">
									<path d="M6.5 8.25C7.743 8.25 8.75 7.243 8.75 6C8.75 4.757 7.743 3.75 6.5 3.75C5.257 3.75 4.25 4.757 4.25 6C4.25 7.243 5.257 8.25 6.5 8.25Z" stroke={isDark ? 'rgba(255,255,255,0.15)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<path d="M1.75 14.25C1.75 11.767 3.878 9.75 6.5 9.75C7.28 9.75 8.017 9.934 8.667 10.261" stroke={isDark ? 'rgba(255,255,255,0.15)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<path d="M13.25 16.25C15.045 16.25 16.5 14.795 16.25 13C16.25 11.205 14.795 9.75 13 9.75C11.205 9.75 9.75 11.205 9.75 13C9.75 14.795 11.205 16.25 13 16.25" stroke={isDark ? 'rgba(255,255,255,0.15)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<line x1="13" y1="11.25" x2="13" y2="14.75" stroke={isDark ? 'rgba(255,255,255,0.15)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<line x1="11.25" y1="13" x2="14.75" y2="13" stroke={isDark ? 'rgba(255,255,255,0.15)' : 'rgba(161,161,170,1)'} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								</svg>
							</div>
						<p class="mt-4 text-[13px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Enter a group name to see preview</p>
					</div>
				{:else}
					<!-- Group preview card -->
					<div class="rounded-xl border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-5">
						<!-- Header -->
						<div class="flex items-start justify-between">
							<div>
								<p class="text-[10px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Group</p>
								<p class="mt-1 text-[11px] {isDark ? 'text-white/15' : 'text-zinc-400'}">Draft</p>
							</div>
							<img src="/logo-gold.png" alt="" class="h-6 w-6 opacity-40" />
						</div>

						<div class="my-4 border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-200'}"></div>

						<!-- Group Info -->
						<div class="mb-4">
							<p class="mt-1.5 text-[14px] font-semibold {isDark ? 'text-white/80' : 'text-zinc-700'}">{groupName}</p>
							{#if groupDescription}
								<p class="mt-1 text-[12px] {isDark ? 'text-white/40' : 'text-zinc-500'}">{groupDescription}</p>
							{/if}
						</div>

						<!-- Contribution -->
						<div class="mb-4 rounded-lg bg-emerald-500/[0.06] px-4 py-3">
							<p class="text-[10px] font-medium uppercase tracking-[0.15em] text-emerald-500/60">Contribution</p>
							<p class="mt-1 font-['Instrument_Serif'] text-2xl italic text-emerald-400">
								{parsedAmount > 0 ? formatKES(parsedAmount) : 'KES 0'} / {contributionFrequency}
							</p>
						</div>

						<!-- Members -->
						<div class="space-y-3">
							<div>
								<p class="text-[10px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/20' : 'text-zinc-400'}">Members ({members.filter(m => m.name).length})</p>
								<div class="mt-2 space-y-1">
									{#each members.filter(m => m.name) as member}
										<p class="text-[12px] {isDark ? 'text-white/40' : 'text-zinc-500'}">{member.name}</p>
									{/each}
								</div>
							</div>
						</div>

						<div class="my-4 border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-200'}"></div>

						<!-- Footer -->
						<div class="flex items-center justify-between">
							<p class="text-[10px] {isDark ? 'text-white/15' : 'text-zinc-400'}">Powered by CashFlow AI</p>
							<span class="rounded-full border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} px-2 py-0.5 text-[10px] {isDark ? 'text-white/20' : 'text-zinc-400'}">Chama Smart</span>
						</div>
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>
