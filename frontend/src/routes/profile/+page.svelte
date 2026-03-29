<script lang="ts">
	import { auth } from '$lib/stores/auth';
	import { api } from '$lib/api';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { theme } from '$lib/stores/theme';
	import { showError, showSuccess } from '$lib/stores/toast';
	import { getAvatarUrl } from '$lib/avatar';

	const isDark = $derived($theme === 'dark');

	// Profile state
	let profileLoading = $state(true);
	let profileSaving = $state(false);
	let businessName = $state('');
	let phone = $state('');
	let mpesaShortcode = $state('');

	// Password state
	let currentPassword = $state('');
	let newPassword = $state('');
	let confirmPassword = $state('');
	let passwordSaving = $state(false);

	// Sessions state
	let sessions = $state<Session[]>([]);
	let sessionsLoading = $state(true);
	let revokingId = $state<string | null>(null);
	let revokingAll = $state(false);

	// Visibility animation
	let visible = $state(false);

	interface Session {
		id: string;
		device_name: string;
		ip_address: string;
		created_at: string;
		last_seen_at: string;
		is_current: boolean;
	}

	onMount(async () => {
		if (!$auth.token) { goto('/login'); return; }
		await Promise.all([loadProfile(), loadSessions()]);
		setTimeout(() => (visible = true), 50);
	});

	async function loadProfile() {
		try {
			const data = await api<{ name: string; phone: string; mpesa_shortcode: string }>('/profile/');
			businessName = data.name ?? '';
			phone = data.phone ?? '';
			mpesaShortcode = data.mpesa_shortcode ?? '';
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to load profile');
		} finally {
			profileLoading = false;
		}
	}

	async function loadSessions() {
		try {
			const data = await api<Session[]>('/profile/sessions');
			sessions = data ?? [];
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to load sessions');
		} finally {
			sessionsLoading = false;
		}
	}

	async function saveProfile(e: Event) {
		e.preventDefault();
		profileSaving = true;
		try {
			await api('/profile/', {
				method: 'PATCH',
				body: JSON.stringify({
					name: businessName || undefined,
					phone: phone || undefined,
					mpesa_shortcode: mpesaShortcode || undefined
				})
			});
			showSuccess('Profile updated');
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to update profile');
		} finally {
			profileSaving = false;
		}
	}

	async function changePassword(e: Event) {
		e.preventDefault();
		if (newPassword !== confirmPassword) {
			showError('New passwords do not match');
			return;
		}
		if (newPassword.length < 8) {
			showError('Password must be at least 8 characters');
			return;
		}
		passwordSaving = true;
		try {
			await api('/auth/change-password', {
				method: 'POST',
				body: JSON.stringify({
					current_password: currentPassword,
					new_password: newPassword
				})
			});
			showSuccess('Password changed successfully');
			currentPassword = '';
			newPassword = '';
			confirmPassword = '';
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to change password');
		} finally {
			passwordSaving = false;
		}
	}

	async function revokeSession(id: string) {
		revokingId = id;
		try {
			await api(`/profile/sessions/${id}`, { method: 'DELETE' });
			sessions = sessions.filter(s => s.id !== id);
			showSuccess('Session revoked');
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to revoke session');
		} finally {
			revokingId = null;
		}
	}

	async function revokeAllOtherSessions() {
		revokingAll = true;
		try {
			await api('/profile/sessions', { method: 'DELETE' });
			sessions = sessions.filter(s => s.is_current);
			showSuccess('All other sessions revoked');
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Failed to revoke sessions');
		} finally {
			revokingAll = false;
		}
	}

	function timeAgo(dateStr: string): string {
		const date = new Date(dateStr);
		const now = new Date();
		const diffMs = now.getTime() - date.getTime();
		const diffSecs = Math.floor(diffMs / 1000);
		const diffMins = Math.floor(diffSecs / 60);
		const diffHours = Math.floor(diffMins / 60);
		const diffDays = Math.floor(diffHours / 24);
		const diffWeeks = Math.floor(diffDays / 7);
		const diffMonths = Math.floor(diffDays / 30);

		if (diffSecs < 60) return 'just now';
		if (diffMins < 60) return `${diffMins} minute${diffMins !== 1 ? 's' : ''} ago`;
		if (diffHours < 24) return `${diffHours} hour${diffHours !== 1 ? 's' : ''} ago`;
		if (diffDays < 7) return `${diffDays} day${diffDays !== 1 ? 's' : ''} ago`;
		if (diffWeeks < 4) return `${diffWeeks} week${diffWeeks !== 1 ? 's' : ''} ago`;
		if (diffMonths < 12) return `${diffMonths} month${diffMonths !== 1 ? 's' : ''} ago`;
		return date.toLocaleDateString();
	}

	function isMobile(deviceName: string): boolean {
		return /mobile|phone|android|ios|iphone|ipad|tablet/i.test(deviceName);
	}

	const otherSessions = $derived(sessions.filter(s => !s.is_current));
</script>

<svelte:head>
	<title>Profile & Security — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="mx-auto max-w-7xl px-4 py-8 md:px-8" style="font-family: 'DM Sans', sans-serif;">
	<!-- Header -->
	<div class="mb-8">
		<a
			href="/dashboard"
			class="mb-4 inline-flex items-center gap-2 text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'} transition-colors {isDark ? 'hover:text-white/60' : 'hover:text-zinc-700'}"
		>
			<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
				<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
			</svg>
			Back to Dashboard
		</a>
		<p class="mb-1 text-[12px] font-medium uppercase tracking-[0.15em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Account</p>
		<div class="flex items-center gap-4">
			<img src={getAvatarUrl($auth.name || $auth.email || 'user')} alt="Avatar" class="h-12 w-12 rounded-full" />
			<div>
				<h1 class="font-['Instrument_Serif'] text-3xl tracking-tight {isDark ? 'text-white' : 'text-zinc-900'} md:text-4xl">Profile & Security</h1>
				<p class="mt-0.5 text-[14px] {isDark ? 'text-white/40' : 'text-zinc-500'}">{$auth.email}</p>
			</div>
		</div>
	</div>

	{#if profileLoading && sessionsLoading}
		<!-- Skeleton -->
		<div class="animate-pulse">
			<div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
				<div class="space-y-4 lg:col-span-2">
					<div class="h-64 rounded-2xl {isDark ? 'bg-white/[0.02]' : 'bg-white'}"></div>
					<div class="h-48 rounded-2xl {isDark ? 'bg-white/[0.02]' : 'bg-white'}"></div>
				</div>
				<div class="h-80 rounded-2xl {isDark ? 'bg-white/[0.02]' : 'bg-white'}"></div>
			</div>
		</div>
	{:else}
		<div class="grid grid-cols-1 gap-6 lg:grid-cols-3">
			<!-- Left column: Profile + Password -->
			<div class="space-y-6 lg:col-span-2">

				<!-- Profile card -->
				<form
					onsubmit={saveProfile}
					class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}"
				>
					<span class="mb-5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Business Information</span>

					<div class="space-y-4">
						<div>
							<label for="businessName" class="mb-2 block text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">Business Name</label>
							<input
								id="businessName"
								type="text"
								bind:value={businessName}
								placeholder="Acme Ltd."
								class="w-full rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.03]' : 'border-zinc-200 bg-white'} px-4 py-3 text-[14px] {isDark ? 'text-white placeholder-white/20' : 'text-zinc-900 placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-white'}"
							/>
						</div>

						<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
							<div>
								<label for="phone" class="mb-2 block text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">Phone Number</label>
								<input
									id="phone"
									type="tel"
									bind:value={phone}
									placeholder="0712 345 678"
									class="w-full rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.03]' : 'border-zinc-200 bg-white'} px-4 py-3 text-[14px] {isDark ? 'text-white placeholder-white/20' : 'text-zinc-900 placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-white'}"
								/>
							</div>
							<div>
								<label for="mpesaShortcode" class="mb-2 block text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">M-Pesa Shortcode</label>
								<input
									id="mpesaShortcode"
									type="text"
									bind:value={mpesaShortcode}
									placeholder="174379"
									class="w-full rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.03]' : 'border-zinc-200 bg-white'} px-4 py-3 text-[14px] {isDark ? 'text-white placeholder-white/20' : 'text-zinc-900 placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-white'}"
								/>
							</div>
						</div>
					</div>

					<div class="mt-6 flex justify-end">
						<button
							type="submit"
							disabled={profileSaving}
							class="rounded-xl bg-emerald-500 px-6 py-2.5 text-[13px] font-semibold text-zinc-950 transition-colors hover:bg-emerald-600 disabled:opacity-50"
						>
							{#if profileSaving}
								<div class="flex items-center gap-2">
									<div class="h-3.5 w-3.5 animate-spin rounded-full border-2 border-zinc-950 border-t-transparent"></div>
									Saving…
								</div>
							{:else}
								Save Changes
							{/if}
						</button>
					</div>
				</form>

				<!-- Change password card -->
				<form
					onsubmit={changePassword}
					class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6 transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}"
					style="transition-delay: 50ms;"
				>
					<span class="mb-5 block text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Change Password</span>

					<div class="space-y-4">
						<div>
							<label for="currentPassword" class="mb-2 block text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">Current Password</label>
							<input
								id="currentPassword"
								type="password"
								bind:value={currentPassword}
								required
								autocomplete="current-password"
								placeholder="••••••••"
								class="w-full rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.03]' : 'border-zinc-200 bg-white'} px-4 py-3 text-[14px] {isDark ? 'text-white placeholder-white/20' : 'text-zinc-900 placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-white'}"
							/>
						</div>

						<div class="grid grid-cols-1 gap-4 md:grid-cols-2">
							<div>
								<label for="newPassword" class="mb-2 block text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">New Password</label>
								<input
									id="newPassword"
									type="password"
									bind:value={newPassword}
									required
									autocomplete="new-password"
									placeholder="••••••••"
									class="w-full rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.03]' : 'border-zinc-200 bg-white'} px-4 py-3 text-[14px] {isDark ? 'text-white placeholder-white/20' : 'text-zinc-900 placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-white'}"
								/>
							</div>
							<div>
								<label for="confirmPassword" class="mb-2 block text-[11px] font-medium {isDark ? 'text-white/60' : 'text-zinc-600'}">Confirm New Password</label>
								<input
									id="confirmPassword"
									type="password"
									bind:value={confirmPassword}
									required
									autocomplete="new-password"
									placeholder="••••••••"
									class="w-full rounded-xl border {isDark ? 'border-white/[0.06] bg-white/[0.03]' : 'border-zinc-200 bg-white'} px-4 py-3 text-[14px] {isDark ? 'text-white placeholder-white/20' : 'text-zinc-900 placeholder-zinc-400'} outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'focus:bg-white/[0.05]' : 'focus:bg-white'}"
								/>
							</div>
						</div>

						{#if newPassword && confirmPassword && newPassword !== confirmPassword}
							<p class="text-[12px] text-red-400">Passwords do not match</p>
						{/if}
					</div>

					<div class="mt-6 flex items-center justify-between">
						<p class="text-[12px] {isDark ? 'text-white/25' : 'text-zinc-400'}">Minimum 8 characters</p>
						<button
							type="submit"
							disabled={passwordSaving || !currentPassword || !newPassword || !confirmPassword || newPassword !== confirmPassword}
							class="rounded-xl bg-emerald-500 px-6 py-2.5 text-[13px] font-semibold text-zinc-950 transition-colors hover:bg-emerald-600 disabled:opacity-50"
						>
							{#if passwordSaving}
								<div class="flex items-center gap-2">
									<div class="h-3.5 w-3.5 animate-spin rounded-full border-2 border-zinc-950 border-t-transparent"></div>
									Updating…
								</div>
							{:else}
								Update Password
							{/if}
						</button>
					</div>
				</form>
			</div>

			<!-- Right column: Sessions -->
			<div class="transition-all {visible ? 'translate-y-0 opacity-100' : 'translate-y-3 opacity-0'}" style="transition-delay: 100ms;">
				<div class="rounded-2xl border {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-white'} p-6">
					<div class="mb-5 flex items-center justify-between">
						<span class="text-[11px] font-medium uppercase tracking-[0.12em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Active Sessions</span>
						<span class="rounded-full {isDark ? 'bg-white/[0.04]' : 'bg-zinc-100'} px-2 py-0.5 text-[11px] font-medium {isDark ? 'text-white/40' : 'text-zinc-500'}">{sessions.length}</span>
					</div>

					{#if sessionsLoading}
						<div class="space-y-3 animate-pulse">
							{#each Array(3) as _}
								<div class="h-16 rounded-xl {isDark ? 'bg-white/[0.03]' : 'bg-zinc-100'}"></div>
							{/each}
						</div>
					{:else if sessions.length === 0}
						<div class="py-8 text-center">
							<div class="mx-auto mb-3 flex h-10 w-10 items-center justify-center rounded-full {isDark ? 'bg-white/[0.03]' : 'bg-zinc-100'}">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 {isDark ? 'text-white/20' : 'text-zinc-400'}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
									<path stroke-linecap="round" stroke-linejoin="round" d="M9 17.25v1.007a3 3 0 01-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0115 18.257V17.25m6-12V15a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 15V5.25m18 0A2.25 2.25 0 0018.75 3H5.25A2.25 2.25 0 003 5.25m18 0H3" />
								</svg>
							</div>
							<p class="text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'}">No active sessions</p>
						</div>
					{:else}
						<div class="space-y-2">
							{#each sessions as session (session.id)}
								<div class="rounded-xl border {isDark ? 'border-white/[0.04] bg-white/[0.01]' : 'border-zinc-100 bg-zinc-50'} p-3.5 transition-all {isDark ? 'hover:border-white/[0.07]' : 'hover:border-zinc-200'}">
									<div class="flex items-start gap-3">
										<!-- Device icon -->
										<div class="mt-0.5 flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-lg {session.is_current ? 'bg-emerald-500/10' : (isDark ? 'bg-white/[0.04]' : 'bg-zinc-200')}">
											{#if isMobile(session.device_name)}
												<!-- Mobile icon -->
												<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {session.is_current ? 'text-emerald-400' : (isDark ? 'text-white/30' : 'text-zinc-400')}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
													<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 15.75h3" />
												</svg>
											{:else}
												<!-- Desktop/laptop icon -->
												<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 {session.is_current ? 'text-emerald-400' : (isDark ? 'text-white/30' : 'text-zinc-400')}" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
													<path stroke-linecap="round" stroke-linejoin="round" d="M9 17.25v1.007a3 3 0 01-.879 2.122L7.5 21h9l-.621-.621A3 3 0 0115 18.257V17.25m6-12V15a2.25 2.25 0 01-2.25 2.25H5.25A2.25 2.25 0 013 15V5.25m18 0A2.25 2.25 0 0018.75 3H5.25A2.25 2.25 0 003 5.25m18 0H3" />
												</svg>
											{/if}
										</div>

										<!-- Info -->
										<div class="min-w-0 flex-1">
											<div class="flex items-center gap-2">
												<p class="truncate text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-800'}">{session.device_name || 'Unknown device'}</p>
												{#if session.is_current}
													<span class="flex-shrink-0 rounded-full bg-emerald-500/15 px-2 py-0.5 text-[10px] font-semibold text-emerald-400">Current</span>
												{/if}
											</div>
											<p class="mt-0.5 text-[11px] {isDark ? 'text-white/30' : 'text-zinc-400'} font-mono">{session.ip_address}</p>
											<p class="mt-0.5 text-[11px] {isDark ? 'text-white/25' : 'text-zinc-400'}">{timeAgo(session.last_seen_at)}</p>
										</div>

										<!-- Revoke button -->
										{#if !session.is_current}
											<button
												onclick={() => revokeSession(session.id)}
												disabled={revokingId === session.id}
												class="flex-shrink-0 rounded-lg px-2.5 py-1.5 text-[11px] font-medium text-red-400/70 transition-colors hover:bg-red-500/[0.08] hover:text-red-400 disabled:opacity-50"
											>
												{#if revokingId === session.id}
													<div class="h-3 w-3 animate-spin rounded-full border border-red-400 border-t-transparent"></div>
												{:else}
													Revoke
												{/if}
											</button>
										{/if}
									</div>
								</div>
							{/each}
						</div>

						{#if otherSessions.length > 1}
							<div class="mt-4 border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} pt-4">
								<button
									onclick={revokeAllOtherSessions}
									disabled={revokingAll}
									class="w-full rounded-xl border {isDark ? 'border-red-500/20 bg-red-500/[0.04]' : 'border-red-200 bg-red-50'} py-2.5 text-[12px] font-medium text-red-400 transition-colors hover:bg-red-500/[0.08] disabled:opacity-50"
								>
									{#if revokingAll}
										<div class="flex items-center justify-center gap-2">
											<div class="h-3 w-3 animate-spin rounded-full border border-red-400 border-t-transparent"></div>
											Revoking…
										</div>
									{:else}
										Revoke all other sessions
									{/if}
								</button>
							</div>
						{/if}
					{/if}
				</div>
			</div>
		</div>
	{/if}
</div>
