<script lang="ts">
	import { toggleTheme } from '$lib/stores/theme';

	interface Props {
		isDark: boolean;
	}

	let { isDark }: Props = $props();
</script>

<!-- LANDING NAV -->
<header class="fixed top-0 left-0 right-0 z-50">
	<div class="mx-auto max-w-7xl px-6 py-5">
		<div class="flex items-center justify-between rounded-2xl border px-6 py-3 backdrop-blur-xl transition-colors {isDark ? 'border-white/[0.06] bg-zinc-950/60' : 'border-zinc-200 bg-white/80'}">
			<a href="/" class="flex items-center gap-2.5">
				<img src={isDark ? '/logo-gold.png' : '/logo-dark.png'} alt="CashFlow AI" class="h-8 w-8" />
				<span class="text-[15px] font-semibold tracking-tight {isDark ? 'text-white/90' : 'text-zinc-900'}">CashFlow AI</span>
			</a>

			<nav class="hidden items-center gap-7 md:flex">
				<a href="#features" class="text-[13px] font-medium transition-colors {isDark ? 'text-white/50 hover:text-white/90' : 'text-zinc-500 hover:text-zinc-900'}">Features</a>
				<a href="#how-it-works" class="text-[13px] font-medium transition-colors {isDark ? 'text-white/50 hover:text-white/90' : 'text-zinc-500 hover:text-zinc-900'}">How It Works</a>
				<a href="#integrations" class="text-[13px] font-medium transition-colors {isDark ? 'text-white/50 hover:text-white/90' : 'text-zinc-500 hover:text-zinc-900'}">Integrations</a>
			</nav>

			<div class="flex items-center gap-3">
				<button
					onclick={toggleTheme}
					class="rounded-lg p-2 transition-colors {isDark ? 'text-white/40 hover:text-white/80 hover:bg-white/[0.06]' : 'text-zinc-400 hover:text-zinc-700 hover:bg-zinc-100'}"
					title="Toggle dark mode"
				>
					{#if isDark}
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
						</svg>
					{:else}
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />
						</svg>
					{/if}
				</button>
				<a href="/login" class="text-[13px] font-medium transition-colors {isDark ? 'text-white/60 hover:text-white' : 'text-zinc-600 hover:text-zinc-900'}">Login</a>
				<a href="/register" class="rounded-lg px-4 py-1.5 text-[13px] font-semibold transition-all {isDark ? 'bg-white text-zinc-950 hover:bg-white/90' : 'bg-zinc-900 text-white hover:bg-zinc-800'}">Sign Up</a>
			</div>
		</div>
	</div>
</header>
