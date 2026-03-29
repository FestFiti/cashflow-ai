<script lang="ts">
	import { goto } from '$app/navigation'
	import { page } from '$app/stores'
	import { api } from '$lib/api'
	import { login } from '$lib/stores/auth'
	import { showError } from '$lib/stores/toast'
	import HeroBlob from '$lib/components/HeroBlob.svelte'
	import HeroBlobLight from '$lib/components/HeroBlobLight.svelte'
	import { theme } from '$lib/stores/theme'

	const isDark = $derived($theme === 'dark')

	let email = $state('')
	let password = $state('')
	let loading = $state(false)
	let showPassword = $state(false)

	const redirectTo = $derived($page.url.searchParams.get('redirect') || '/dashboard')

	async function handleSubmit(e: Event) {
		e.preventDefault()
		loading = true
		try {
			const res = await api<{
				access_token: string
				business_id: string
				name: string
				email: string
			}>('/auth/login', {
				method: 'POST',
				body: JSON.stringify({ email, password }),
			})
			login(res.access_token, res.business_id, res.name, res.email)
			goto(redirectTo)
		} catch (err) {
			showError(err instanceof Error ? err.message : 'Login failed')
		} finally {
			loading = false
		}
	}
</script>

<svelte:head>
	<title>Login — CashFlow AI</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link
		href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&display=swap"
		rel="stylesheet"
	/>
</svelte:head>

<div class="grid min-h-screen grid-cols-1 lg:grid-cols-2">
	<!-- Left: Form -->
	<div class="flex flex-col justify-center px-6 py-12 lg:px-16 {isDark ? '' : 'bg-white'}">
		<div class="mx-auto w-full max-w-sm">
			<a href="/" class="mb-10 inline-flex items-center gap-2.5">
				<img src={isDark ? '/logo-gold.png' : '/logo-dark.png'} alt="CashFlow AI" class="h-9 w-9" />
				<span class="text-lg font-semibold tracking-tight {isDark ? 'text-white/90' : 'text-zinc-900'}">CashFlow AI</span>
			</a>

			<h1 class="mb-2 font-['Instrument_Serif'] text-3xl {isDark ? 'text-white' : 'text-zinc-900'}">Welcome back</h1>
			<p class="mb-8 text-sm {isDark ? 'text-white/35' : 'text-zinc-500'}" style="font-family: 'DM Sans', sans-serif;">
				Sign in to manage your cash flow
			</p>

			<form onsubmit={handleSubmit} class="space-y-5" style="font-family: 'DM Sans', sans-serif;">
				<div>
					<label for="email" class="mb-1.5 block text-[13px] font-medium {isDark ? 'text-white/40' : 'text-zinc-500'}">Email</label
					>
					<input
						id="email"
						type="email"
						bind:value={email}
						required
						class="w-full rounded-xl border px-4 py-3 text-[14px] outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'border-white/[0.06] bg-white/[0.03] text-white placeholder-white/20 focus:bg-white/[0.05]' : 'border-zinc-300 bg-zinc-50 text-zinc-900 placeholder-zinc-400 focus:bg-white'}"
						placeholder="you@business.com"
					/>
				</div>

				<div>
					<div class="mb-1.5 flex items-center justify-between">
						<label for="password" class="text-[13px] font-medium {isDark ? 'text-white/40' : 'text-zinc-500'}">Password</label>
						<a
							href="/forgot-password"
							class="text-[12px] text-emerald-400/70 hover:text-emerald-400">Forgot password?</a
						>
					</div>
					<div class="relative">
						<input
							id="password"
							type={showPassword ? 'text' : 'password'}
							bind:value={password}
							required
							class="w-full rounded-xl border px-4 py-3 pr-10 text-[14px] outline-none transition-colors focus:border-emerald-500/50 {isDark ? 'border-white/[0.06] bg-white/[0.03] text-white placeholder-white/20 focus:bg-white/[0.05]' : 'border-zinc-300 bg-zinc-50 text-zinc-900 placeholder-zinc-400 focus:bg-white'}"
							placeholder="Enter your password"
						/>
						<button
							type="button"
							onclick={() => (showPassword = !showPassword)}
							class="absolute right-3 top-1/2 -translate-y-1/2 {isDark ? 'text-white/20 hover:text-white/50' : 'text-zinc-400 hover:text-zinc-600'}"
						>
							{#if showPassword}
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="h-4 w-4"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
									stroke-width="1.5"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88"
									/>
								</svg>
							{:else}
								<svg
									xmlns="http://www.w3.org/2000/svg"
									class="h-4 w-4"
									fill="none"
									viewBox="0 0 24 24"
									stroke="currentColor"
									stroke-width="1.5"
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
							{/if}
						</button>
					</div>
				</div>

				<button
					type="submit"
					disabled={loading}
					class="group w-full rounded-xl bg-emerald-900 py-3 text-[14px] text-zinc-100 transition-all hover:bg-emerald-950 cursor-pointer hover:text-zinc-200 border-emerald-900 border hover:border-gray-600/20 disabled:opacity-50"
				>
					{loading ? 'Signing in...' : 'Sign In'}
				</button>

				<p class="text-center text-[13px] {isDark ? 'text-white/30' : 'text-zinc-500'}">
					Don't have an account?
					<a href="/register" class="text-emerald-400/80 hover:text-emerald-400">Register</a>
				</p>
			</form>
		</div>
	</div>

	<!-- Right: Blob -->
	<div
		class="relative hidden overflow-hidden lg:block"
		style="background: {$theme === 'dark' ? 'radial-gradient(ellipse at 50% 50%, #1a1a2e 0%, #0a0a0f 60%, #050508 100%)' : 'radial-gradient(ellipse at 50% 50%, #f0fdf4 0%, #ecfdf5 40%, #ffffff 100%)'};"
	>
		<div class="pointer-events-none absolute inset-0">
			<div
				class="absolute left-1/2 top-1/2 h-[500px] w-[700px] -translate-x-1/2 -translate-y-1/2 rounded-full opacity-25"
				style="background: radial-gradient(ellipse, {$theme === 'dark' ? 'rgba(255,180,50,0.2) 0%, rgba(100,60,10,0.08) 40%' : 'rgba(16,185,129,0.2) 0%, rgba(16,185,129,0.05) 40%'}, transparent 70%);"
			></div>
		</div>
		{#if $theme === 'dark'}
			<HeroBlob />
		{:else}
			<HeroBlobLight />
		{/if}
		<div
			class="pointer-events-none absolute inset-0 opacity-[0.02]"
			style="background-image: radial-gradient(circle, white 1px, transparent 1px); background-size: 24px 24px;"
		></div>
		<!-- Horizontal gradient fade from form into blob -->
		<div class="pointer-events-none absolute inset-y-0 left-0 w-32 {isDark ? 'bg-gradient-to-r from-zinc-950 to-transparent' : 'bg-gradient-to-r from-white to-transparent'}"></div>
		<!-- Vertical gradient fade at bottom -->
		<div class="pointer-events-none absolute left-0 -bottom-0 right-0 h-44 {isDark ? 'bg-gradient-to-t from-zinc-950 to-transparent' : 'bg-gradient-to-t from-white to-transparent'}"></div>
	</div>
</div>
