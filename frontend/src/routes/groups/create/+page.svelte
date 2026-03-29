<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let groupName = $state('');
	let groupDescription = $state('');
	let contributionAmount = $state('');
	let contributionFrequency = $state('monthly');
	let contributionDay = $state('1');
	let members = $state([{ name: '', phone: '', email: '' }]);
	let loading = $state(false);
	let error = $state('');
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
			error = 'Please fill all required fields';
			return;
		}

		loading = true;
		error = '';
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
			error = err instanceof Error ? err.message : 'Failed to create group';
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
	<a href="/dashboard" class="mb-6 inline-flex items-center gap-1.5 text-[13px] text-white/25 transition-colors hover:text-white/50">
		<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
			<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
		</svg>
		Back to dashboard
	</a>
	<div class="mb-8">
		<p class="mb-1 text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Create</p>
		<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight text-white">
			Create <span class="italic text-emerald-400">Group</span>
		</h1>
	</div>

	<div class="grid grid-cols-1 gap-6 lg:grid-cols-12">
		<!-- LEFT: Form -->
		<div class="lg:col-span-7">
			{#if error}
				<div class="mb-4 rounded-xl border border-red-500/20 bg-red-500/[0.05] px-4 py-3 text-[13px] text-red-400">{error}</div>
			{/if}

			<form onsubmit={handleCreateGroup} class="rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="space-y-5">
					<!-- Group Information -->
					<div>
						<label for="groupName" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Group Name</label>
						<input id="groupName" type="text" bind:value={groupName} required class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30" placeholder="e.g., Office Chama, Investment Club" />
					</div>

					<div>
						<label for="groupDescription" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Description</label>
						<textarea id="groupDescription" bind:value={groupDescription} rows={3} class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30" placeholder="What is this group for? What are the goals?"></textarea>
					</div>

					<!-- Contribution Settings -->
					<div class="grid grid-cols-1 gap-5 md:grid-cols-2">
						<div>
							<label for="contributionAmount" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Contribution Amount (KES)</label>
							<input id="contributionAmount" type="number" bind:value={contributionAmount} required min="0" step="0.01" class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30" placeholder="5000" />
						</div>
						<div>
							<label for="contributionFrequency" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Frequency</label>
							<select id="contributionFrequency" bind:value={contributionFrequency} class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30">
								<option value="daily">Daily</option>
								<option value="weekly">Weekly</option>
								<option value="monthly">Monthly</option>
								<option value="quarterly">Quarterly</option>
							</select>
						</div>
					</div>

					<div>
						<label for="contributionDay" class="mb-1.5 block text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">
							{contributionFrequency === 'monthly' ? 'Day of Month' : contributionFrequency === 'weekly' ? 'Day of Week' : 'Time Period'}
						</label>
						<select id="contributionDay" bind:value={contributionDay} class="w-full rounded-xl border border-white/[0.04] bg-white/[0.02] px-4 py-2.5 text-[13px] text-white outline-none placeholder-white/15 focus:border-emerald-500/30">
							{#if contributionFrequency === 'monthly'}
								{#each Array.from({length: 31}, (_, i) => i + 1) as day}
									<option value={day}>{day}{day === 1 ? 'st' : day === 2 ? 'nd' : day === 3 ? 'rd' : 'th'}</option>
								{/each}
							{:else if contributionFrequency === 'weekly'}
								<option value="1">Monday</option>
								<option value="2">Tuesday</option>
								<option value="3">Wednesday</option>
								<option value="4">Thursday</option>
								<option value="5">Friday</option>
								<option value="6">Saturday</option>
								<option value="7">Sunday</option>
							{:else}
								<option value="1">1st Period</option>
								<option value="2">2nd Period</option>
								<option value="3">3rd Period</option>
								<option value="4">4th Period</option>
							{/if}
						</select>
					</div>

					<!-- Members -->
					<div>
						<div class="mb-4 flex items-center justify-between">
							<label class="text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Group Members</label>
							<button
								type="button"
								onclick={addMember}
								class="rounded-lg border border-white/[0.06] px-3 py-1 text-[11px] font-medium text-white transition-colors hover:bg-white/[0.05]"
							>
								+ Add Member
							</button>
						</div>
						
						<div class="space-y-3">
							{#each members as member, index}
								<div class="rounded-xl border border-white/[0.04] bg-white/[0.01] p-4">
									<div class="grid grid-cols-3 gap-3">
										<div>
											<input
												type="text"
												bind:value={member.name}
												placeholder="Full Name *"
												class="w-full rounded-lg border border-white/[0.06] bg-white/[0.02] px-3 py-2 text-sm text-white placeholder-white/20 outline-none transition-colors focus:border-emerald-500/50 focus:bg-white/[0.05]"
												required
											/>
										</div>
										<div>
											<input
												type="tel"
												bind:value={member.phone}
												placeholder="Phone *"
												class="w-full rounded-lg border border-white/[0.06] bg-white/[0.02] px-3 py-2 text-sm text-white placeholder-white/20 outline-none transition-colors focus:border-emerald-500/50 focus:bg-white/[0.05]"
												required
											/>
										</div>
										<div class="flex gap-2">
											<input
												type="email"
												bind:value={member.email}
												placeholder="Email (optional)"
												class="flex-1 rounded-lg border border-white/[0.06] bg-white/[0.02] px-3 py-2 text-sm text-white placeholder-white/20 outline-none transition-colors focus:border-emerald-500/50 focus:bg-white/[0.05]"
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
			<div class="sticky top-24 rounded-2xl border border-white/[0.04] bg-white/[0.02] p-6 transition-all duration-500 delay-150 {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-5 flex items-center justify-between">
					<span class="text-[11px] font-medium uppercase tracking-[0.12em] text-white/25">Group Preview</span>
					<div class="flex h-6 w-6 items-center justify-center rounded-md bg-white/[0.03]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 text-white/20" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719" />
						</svg>
					</div>
				</div>

				{#if !groupName}
					<!-- Empty preview -->
					<div class="flex flex-col items-center py-12 text-center">
						<div class="flex h-12 w-12 items-center justify-center rounded-lg bg-white/[0.03]">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-white/15" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197A5.971 5.971 0 016 18.72v-2.007m0 0V18.72v-2.007m0 0a5.971 5.971 0 00-.941 3.197M5.058 15.522A5.971 5.971 0 006 18.72v-2.007M5.058 15.522A5.971 5.971 0 016 12.75v2.007m0 0a5.971 5.971 0 00.941 3.197m8.018-8.018a5.971 5.971 0 00-.941-3.197M6 12.75a5.971 5.971 0 01.941-3.197m5.059 5.059a5.971 5.971 0 01-.941 3.197M12 12.75a5.971 5.971 0 01-.941-3.197m0 6.394a5.971 5.971 0 00.941-3.197m0-6.394a5.971 5.971 0 00-.941 3.197" />
							</svg>
						</div>
						<p class="mt-4 text-[13px] text-white/20">Enter a group name to see preview</p>
					</div>
				{:else}
					<!-- Group preview card -->
					<div class="rounded-xl border border-white/[0.06] bg-white/[0.02] p-5">
						<!-- Header -->
						<div class="flex items-start justify-between">
							<div>
								<p class="text-[10px] font-medium uppercase tracking-[0.15em] text-white/20">Group</p>
								<p class="mt-1 text-[11px] text-white/15">Draft</p>
							</div>
							<img src="/logo-gold.png" alt="" class="h-6 w-6 opacity-40" />
						</div>

						<div class="my-4 border-t border-white/[0.04]"></div>

						<!-- Group Info -->
						<div class="mb-4">
							<p class="mt-1.5 text-[14px] font-semibold text-white/80">{groupName}</p>
							{#if groupDescription}
								<p class="mt-1 text-[12px] text-white/40">{groupDescription}</p>
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
								<p class="text-[10px] font-medium uppercase tracking-[0.15em] text-white/20">Members ({members.filter(m => m.name).length})</p>
								<div class="mt-2 space-y-1">
									{#each members.filter(m => m.name) as member}
										<p class="text-[12px] text-white/40">{member.name}</p>
									{/each}
								</div>
							</div>
						</div>

						<div class="my-4 border-t border-white/[0.04]"></div>

						<!-- Footer -->
						<div class="flex items-center justify-between">
							<p class="text-[10px] text-white/15">Powered by CashFlow AI</p>
							<span class="rounded-full border border-white/[0.06] px-2 py-0.5 text-[10px] text-white/20">Chama Smart</span>
						</div>
					</div>
				{/if}
			</div>
		</div>
	</div>
</div>
