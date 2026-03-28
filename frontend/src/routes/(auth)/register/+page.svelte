<script lang="ts">
	import { goto } from '$app/navigation';
	import { api } from '$lib/api';
	import { login } from '$lib/stores/auth';

	let name = $state('');
	let email = $state('');
	let phone = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let error = $state('');
	let loading = $state(false);
	let showPassword = $state(false);

	const passwordChecks = $derived({
		length: password.length >= 8,
		uppercase: /[A-Z]/.test(password),
		lowercase: /[a-z]/.test(password),
		number: /[0-9]/.test(password)
	});
	const passwordValid = $derived(
		passwordChecks.length && passwordChecks.uppercase && passwordChecks.lowercase && passwordChecks.number
	);
	const passwordsMatch = $derived(password === confirmPassword && confirmPassword.length > 0);
	const passwordStrength = $derived(() => {
		let score = 0;
		if (passwordChecks.length) score++;
		if (passwordChecks.uppercase) score++;
		if (passwordChecks.lowercase) score++;
		if (passwordChecks.number) score++;
		if (password.length >= 12) score++;
		return score;
	});

	function getStrengthLabel(score: number) {
		if (score <= 1) return { text: 'Weak', color: 'bg-red-500' };
		if (score <= 2) return { text: 'Fair', color: 'bg-orange-500' };
		if (score <= 3) return { text: 'Good', color: 'bg-yellow-500' };
		return { text: 'Strong', color: 'bg-emerald-500' };
	}

	async function handleSubmit(e: Event) {
		e.preventDefault();
		error = '';

		if (!passwordValid) {
			error = 'Password does not meet requirements';
			return;
		}
		if (!passwordsMatch) {
			error = 'Passwords do not match';
			return;
		}

		loading = true;
		try {
			const res = await api<{ access_token: string; business_id: string; name: string }>(
				'/auth/register',
				{
					method: 'POST',
					body: JSON.stringify({ name, email, phone, password })
				}
			);
			login(res.access_token, res.business_id, res.name, email);
			goto('/dashboard');
		} catch (err) {
			error = err instanceof Error ? err.message : 'Registration failed';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Register — CashFlow AI</title>
</svelte:head>

<div class="flex min-h-screen items-center justify-center px-4 py-8">
	<div class="w-full max-w-md">
		<div class="mb-8 text-center">
			<a href="/" class="mb-6 inline-flex items-center gap-2">
				<div class="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-500/20">
					<span class="text-xl font-bold text-emerald-400">C</span>
				</div>
				<span class="text-xl font-bold tracking-tight">CashFlow AI</span>
			</a>
			<h1 class="mt-4 text-2xl font-bold">Create your account</h1>
			<p class="mt-2 text-sm text-zinc-500">Start automating your cash flow today</p>
		</div>

		<form onsubmit={handleSubmit} class="gradient-bg rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-6 space-y-4">
			{#if error}
				<div class="rounded-lg border border-red-500/20 bg-red-500/10 px-4 py-2 text-sm text-red-400">
					{error}
				</div>
			{/if}

			<div>
				<label for="name" class="mb-1 block text-sm font-medium text-zinc-400">Business Name</label>
				<input
					id="name"
					type="text"
					bind:value={name}
					required
					class="w-full rounded-xl border border-zinc-700 bg-zinc-800/50 px-4 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition-colors focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
					placeholder="Acme Solutions"
				/>
			</div>

			<div>
				<label for="email" class="mb-1 block text-sm font-medium text-zinc-400">Email</label>
				<input
					id="email"
					type="email"
					bind:value={email}
					required
					class="w-full rounded-xl border border-zinc-700 bg-zinc-800/50 px-4 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition-colors focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
					placeholder="you@business.com"
				/>
			</div>

			<div>
				<label for="phone" class="mb-1 block text-sm font-medium text-zinc-400">Phone (M-Pesa)</label>
				<input
					id="phone"
					type="tel"
					bind:value={phone}
					required
					class="w-full rounded-xl border border-zinc-700 bg-zinc-800/50 px-4 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition-colors focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
					placeholder="0712345678"
				/>
			</div>

			<div>
				<label for="password" class="mb-1 block text-sm font-medium text-zinc-400">Password</label>
				<div class="relative">
					<input
						id="password"
						type={showPassword ? 'text' : 'password'}
						bind:value={password}
						required
						class="w-full rounded-xl border border-zinc-700 bg-zinc-800/50 px-4 py-2.5 pr-10 text-sm text-white placeholder-zinc-500 outline-none transition-colors focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
						placeholder="At least 8 characters"
					/>
					<button
						type="button"
						onclick={() => (showPassword = !showPassword)}
						class="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-500 hover:text-zinc-300"
					>
						{#if showPassword}
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
							</svg>
						{:else}
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z" />
								<path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
							</svg>
						{/if}
					</button>
				</div>

				{#if password.length > 0}
					<!-- Strength bar -->
					{@const strength = passwordStrength()}
					{@const label = getStrengthLabel(strength)}
					<div class="mt-2 space-y-2">
						<div class="flex items-center gap-2">
							<div class="flex flex-1 gap-1">
								{#each Array(4) as _, i}
									<div class="h-1 flex-1 rounded-full {i < strength ? label.color : 'bg-zinc-700'} transition-colors"></div>
								{/each}
							</div>
							<span class="text-[11px] text-zinc-500">{label.text}</span>
						</div>
						<ul class="grid grid-cols-2 gap-x-2 gap-y-1">
							{#each [
								{ ok: passwordChecks.length, text: '8+ characters' },
								{ ok: passwordChecks.uppercase, text: 'Uppercase' },
								{ ok: passwordChecks.lowercase, text: 'Lowercase' },
								{ ok: passwordChecks.number, text: 'Number' }
							] as check}
								<li class="flex items-center gap-1.5 text-[11px] {check.ok ? 'text-emerald-400' : 'text-zinc-600'}">
									<svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
										{#if check.ok}
											<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.75l6 6 9-13.5" />
										{:else}
											<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
										{/if}
									</svg>
									{check.text}
								</li>
							{/each}
						</ul>
					</div>
				{/if}
			</div>

			<div>
				<label for="confirmPassword" class="mb-1 block text-sm font-medium text-zinc-400">Confirm Password</label>
				<input
					id="confirmPassword"
					type={showPassword ? 'text' : 'password'}
					bind:value={confirmPassword}
					required
					class="w-full rounded-xl border border-zinc-700 bg-zinc-800/50 px-4 py-2.5 text-sm text-white placeholder-zinc-500 outline-none transition-colors focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 {confirmPassword.length > 0 && !passwordsMatch ? '!border-red-500/50' : ''}"
					placeholder="Repeat your password"
				/>
				{#if confirmPassword.length > 0 && !passwordsMatch}
					<p class="mt-1 text-[11px] text-red-400">Passwords do not match</p>
				{/if}
			</div>

			<button
				type="submit"
				disabled={loading || !passwordValid || !passwordsMatch}
				class="gradient-bg-emerald w-full rounded-xl bg-emerald-600 py-2.5 text-sm font-semibold text-white transition-all hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed"
			>
				{loading ? 'Creating account...' : 'Create Account'}
			</button>

			<p class="text-center text-sm text-zinc-500">
				Already have an account?
				<a href="/login" class="text-emerald-400 hover:text-emerald-300">Sign in</a>
			</p>
		</form>
	</div>
</div>
