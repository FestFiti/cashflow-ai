<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { theme } from '$lib/stores/theme';
	import { api, formatKES } from '$lib/api';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import Select from '$lib/components/Select.svelte';

	const isDark = $derived($theme === 'dark');
	let loading = $state(true);
	let visible = $state(false);
	let phone = $state('');
	let otp = $state('');
	let step = $state<'login' | 'profile' | 'join'>('login');
	let fullName = $state('');
	let photoUrl = $state('');
	let idNumber = $state('');
	let language = $state('english');
	let groupAction = $state<'create' | 'join'>('create');
	let groupName = $state('');
	let contributionAmount = $state('');
	let frequency = $state('weekly');
	let groupCode = $state('');

	onMount(() => {
		if (!$auth.token) {
			// Show onboarding flow
		} else {
			// Show dashboard
			goto('/imarisha/dashboard');
		}
		setTimeout(() => (visible = true), 50);
		loading = false;
	});

	async function handleSendOTP() {
		if (!phone) return;
		// TODO: Send OTP logic
	}

	async function handleVerifyOTP() {
		if (!otp) return;
		// TODO: Verify OTP logic
		step = 'profile';
	}

	async function handleProfileSetup() {
		if (!fullName) return;
		// TODO: Profile setup logic
		step = 'join';
	}

	async function handleCreateGroup() {
		if (!groupName || !contributionAmount) return;
		// TODO: Create group logic
		goto('/imarisha/dashboard');
	}

	async function handleJoinGroup() {
		if (!groupCode) return;
		// TODO: Join group logic
		goto('/imarisha/dashboard');
	}
</script>

<svelte:head>
	<title>Imarisha — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="min-h-screen {isDark ? 'bg-gradient-to-br from-zinc-950 via-zinc-900 to-zinc-950' : 'bg-gradient-to-br from-gray-50 via-white to-gray-50'}" style="font-family: 'DM Sans', sans-serif;">
	{#if step === 'login'}
		<!-- Splash / Login -->
		<div class="flex min-h-screen items-center justify-center px-4">
			<div class="w-full max-w-md transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<!-- Logo and Tagline -->
				<div class="mb-8 text-center">
					<div class="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-emerald-500/10 p-4">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197A5.971 5.971 0 006 18.72v-2.007m0 0V18.72v-2.007m0 0a5.971 5.971 0 00-.941 3.197M5.058 15.522A5.971 5.971 0 006 18.72v-2.007M5.058 15.522A5.971 5.971 0 016 12.75v2.007m0 0a5.971 5.971 0 00.941 3.197m8.018-8.018a5.971 5.971 0 00-.941-3.197M6 12.75a5.971 5.971 0 01.941-3.197m5.059 5.059a5.971 5.971 0 01-.941 3.197M12 12.75a5.971 5.971 0 01-.941-3.197m0 6.394a5.971 5.971 0 00.941-3.197m0-6.394a5.971 5.971 0 00-.941 3.197" />
						</svg>
					</div>
					<h1 class="font-['Instrument_Serif'] text-2xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">Imarisha</h1>
					<p class="mt-2 text-sm {isDark ? 'text-white/60' : 'text-zinc-600'}">Automated Chama Management, Fully Trustworthy</p>
				</div>

				<!-- Phone Login -->
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
					<div class="space-y-4">
						<div>
							<label class="mb-2 block text-sm font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Phone Number</label>
							<input
								type="tel"
								bind:value={phone}
								placeholder="0712345678"
								class="w-full rounded-xl border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.03]' : 'bg-white'} px-4 py-3 {isDark ? 'text-white' : 'text-zinc-900'} {isDark ? 'placeholder-white/20' : 'placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-zinc-50'}"
							/>
						</div>

						{#if otp}
							<div>
								<label class="mb-2 block text-sm font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Enter OTP</label>
								<input
									type="text"
									bind:value={otp}
									placeholder="123456"
									maxlength="6"
									class="w-full rounded-xl border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.03]' : 'bg-white'} px-4 py-3 {isDark ? 'text-white' : 'text-zinc-900'} {isDark ? 'placeholder-white/20' : 'placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-zinc-50'}"
								/>
							</div>
						{/if}

						<button
							onclick={otp ? handleVerifyOTP : handleSendOTP}
							disabled={!phone || (!otp && phone.length < 10)}
							class="w-full rounded-xl bg-emerald-500 py-3 text-sm font-semibold text-zinc-950 transition-colors hover:bg-emerald-600 disabled:opacity-50"
						>
							{otp ? 'Verify & Continue' : 'Send OTP'}
						</button>
					</div>
				</div>

				<!-- Get Started CTA -->
				{#if !otp}
					<div class="mt-6 text-center">
						<button class="rounded-xl border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-8 py-3 text-sm font-medium {isDark ? 'text-white' : 'text-zinc-900'} transition-colors {isDark ? 'hover:bg-white/[0.05]' : 'hover:bg-zinc-50'}">
							Get Started
						</button>
					</div>
				{/if}
			</div>
		</div>
	{:else if step === 'profile'}
		<!-- Profile Setup -->
		<div class="flex min-h-screen items-center justify-center px-4">
			<div class="w-full max-w-md transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-6 text-center">
					<h2 class="font-['Instrument_Serif'] text-xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">Setup Your Profile</h2>
				</div>

				<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
					<div class="space-y-4">
						<div>
							<label class="mb-2 block text-sm font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Full Name</label>
							<input
								type="text"
								bind:value={fullName}
								placeholder="John Kamau"
								class="w-full rounded-xl border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.03]' : 'bg-white'} px-4 py-3 {isDark ? 'text-white' : 'text-zinc-900'} {isDark ? 'placeholder-white/20' : 'placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-zinc-50'}"
								required
							/>
						</div>

						<div>
							<label class="mb-2 block text-sm font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Photo (Optional)</label>
							<div class="flex items-center gap-4">
								{#if photoUrl}
									<img src={photoUrl} alt="Profile" class="h-16 w-16 rounded-full object-cover" />
								{:else}
									<div class="flex h-16 w-16 items-center justify-center rounded-full {isDark ? 'bg-white/[0.05]' : 'bg-zinc-100'}">
										<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 {isDark ? 'text-white/30' : 'text-zinc-400'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
											<path stroke-linecap="round" stroke-linejoin="round" d="M15.75 6a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0zM4.501 20.118a7.5 7.5 0 0014.998 0A17.933 17.933 0 0015.75 15.75M4.501 20.118a7.5 7.5 0 0014.998 0M15.75 15.75v4.5" />
										</svg>
									</div>
								{/if}
								<button class="rounded-lg border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} px-3 py-2 text-xs font-medium {isDark ? 'text-white/60' : 'text-zinc-600'} transition-colors {isDark ? 'hover:bg-white/[0.05]' : 'hover:bg-zinc-50'}">
									{photoUrl ? 'Change' : 'Upload'}
								</button>
							</div>
						</div>

						<div>
							<label class="mb-2 block text-sm font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">ID Number (Optional)</label>
							<input
								type="text"
								bind:value={idNumber}
								placeholder="12345678"
								class="w-full rounded-xl border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.03]' : 'bg-white'} px-4 py-3 {isDark ? 'text-white' : 'text-zinc-900'} {isDark ? 'placeholder-white/20' : 'placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-zinc-50'}"
							/>
						</div>

						<div>
							<label class="mb-2 block text-sm font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Preferred Language</label>
							<Select bind:value={language} options={[
								{ value: 'english', label: 'English' },
								{ value: 'swahili', label: 'Swahili' }
							]} />
						</div>

						<button
							onclick={handleProfileSetup}
							disabled={!fullName}
							class="w-full rounded-xl bg-emerald-500 py-3 text-sm font-semibold text-zinc-950 transition-colors hover:bg-emerald-600 disabled:opacity-50"
						>
							Next
						</button>
					</div>
				</div>
			</div>
		</div>
	{:else if step === 'join'}
		<!-- Create / Join Chama -->
		<div class="flex min-h-screen items-center justify-center px-4">
			<div class="w-full max-w-md transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}">
				<div class="mb-6 text-center">
					<h2 class="font-['Instrument_Serif'] text-xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'}">Join or Create a Chama</h2>
				</div>

				<!-- Action Toggle -->
				<div class="mb-6 flex gap-2 rounded-xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-1">
					<button
						onclick={() => (groupAction = 'create')}
						class="flex-1 rounded-lg px-4 py-2 text-sm font-medium transition-all {groupAction === 'create' ? 'bg-emerald-500 text-zinc-950' : isDark ? 'text-white/60' : 'text-zinc-600'}"
					>
						Create Group
					</button>
					<button
						onclick={() => (groupAction = 'join')}
						class="flex-1 rounded-lg px-4 py-2 text-sm font-medium transition-all {groupAction === 'join' ? 'bg-emerald-500 text-zinc-950' : isDark ? 'text-white/60' : 'text-zinc-600'}"
					>
						Join Group
					</button>
				</div>

				<div class="rounded-2xl border {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.02]' : 'bg-white'} p-6">
					{#if groupAction === 'create'}
						<!-- Create Group Form -->
						<div class="space-y-4">
							<div>
								<label class="mb-2 block text-sm font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Group Name</label>
								<input
									type="text"
									bind:value={groupName}
									placeholder="Office Chama"
									class="w-full rounded-xl border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.03]' : 'bg-white'} px-4 py-3 {isDark ? 'text-white' : 'text-zinc-900'} {isDark ? 'placeholder-white/20' : 'placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-zinc-50'}"
									required
								/>
							</div>

							<div>
								<label class="mb-2 block text-sm font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Contribution Amount (KES)</label>
								<input
									type="number"
									bind:value={contributionAmount}
									placeholder="5000"
									min="0"
									step="100"
									class="w-full rounded-xl border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.03]' : 'bg-white'} px-4 py-3 {isDark ? 'text-white' : 'text-zinc-900'} {isDark ? 'placeholder-white/20' : 'placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-zinc-50'}"
									required
								/>
							</div>

							<div>
								<label class="mb-2 block text-sm font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Frequency</label>
								<Select bind:value={frequency} options={[
									{ value: 'weekly', label: 'Weekly' },
									{ value: 'monthly', label: 'Monthly' },
									{ value: 'custom', label: 'Custom' }
								]} />
							</div>

							<button
								onclick={handleCreateGroup}
								disabled={!groupName || !contributionAmount}
								class="w-full rounded-xl bg-emerald-500 py-3 text-sm font-semibold text-zinc-950 transition-colors hover:bg-emerald-600 disabled:opacity-50"
							>
								Create
							</button>
						</div>
					{:else}
						<!-- Join Group Form -->
						<div class="space-y-4">
							<div>
								<label class="mb-2 block text-sm font-medium {isDark ? 'text-white/80' : 'text-zinc-700'}">Group Code / QR Scan</label>
								<input
									type="text"
									bind:value={groupCode}
									placeholder="Enter group code or scan QR"
									class="w-full rounded-xl border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-white/[0.03]' : 'bg-white'} px-4 py-3 {isDark ? 'text-white' : 'text-zinc-900'} {isDark ? 'placeholder-white/20' : 'placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-zinc-50'}"
									required
								/>
							</div>

							<button
								onclick={handleJoinGroup}
								disabled={!groupCode}
								class="w-full rounded-xl bg-emerald-500 py-3 text-sm font-semibold text-zinc-950 transition-colors hover:bg-emerald-600 disabled:opacity-50"
							>
								Join
							</button>
						</div>
					{/if}
				</div>
			</div>
		</div>
	{/if}
</div>
