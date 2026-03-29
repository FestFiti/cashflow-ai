<script lang="ts">
	import '../app.css';
	import { page } from '$app/stores';
	import { auth, logout } from '$lib/stores/auth';
	import { goto } from '$app/navigation';
	import { onMount, onDestroy } from 'svelte';
	import { connectWs, disconnectWs, wsConnected } from '$lib/stores/ws';
	import NotificationBell from '$lib/components/NotificationBell.svelte';
	import Toaster from '$lib/components/Toaster.svelte';
	import { theme, toggleTheme } from '$lib/stores/theme';
	import { getAvatarUrl } from '$lib/avatar';

	let { children } = $props();
	let mobileMenuOpen = $state(false);
	let userMenuOpen = $state(false);
	const isDark = $derived($theme === 'dark');

	const isAuthPage = $derived(
		$page.url.pathname.startsWith('/login') ||
		$page.url.pathname.startsWith('/register') ||
		$page.url.pathname.startsWith('/forgot-password') ||
		$page.url.pathname.startsWith('/reset-password')
	);
	const isLanding = $derived($page.url.pathname === '/');
	const showNav = $derived(!isAuthPage && !isLanding);

	onMount(() => {
		if ($auth.token) connectWs();
	});

	onDestroy(() => {
		disconnectWs();
	});

	function handleLogout() {
		disconnectWs();
		logout();
		userMenuOpen = false;
		goto('/');
	}

	const navLinks = [
		{ href: '/dashboard', label: 'Dashboard' },
		{ href: '/payments', label: 'Payments' },
		{ href: '/invoices', label: 'Invoices' },
		{ href: '/imarisha', label: 'Imarisha' },
		{ href: '/reports', label: 'Reports' }
	];

	function isActive(href: string, pathname: string) {
		if (href === '/dashboard') return pathname === '/dashboard';
		return pathname.startsWith(href);
	}

	function getInitials(name: string | null): string {
		if (!name) return '?';
		return name.split(' ').map(w => w[0]).join('').toUpperCase().slice(0, 2);
	}
</script>

<svelte:head>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

{#if showNav}
	<header class="sticky top-0 z-50" style="font-family: 'DM Sans', sans-serif;">
		<div class="mx-auto max-w-7xl px-4 py-3 md:px-6">
			<div class="flex items-center justify-between rounded-2xl border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-zinc-950/60' : 'bg-white/80'} px-4 py-2 backdrop-blur-xl md:px-5">
				<!-- Logo -->
				<a href="/dashboard" class="flex items-center gap-2.5">
					<img src="/logo-gold.png" alt="CashFlow AI" class="h-7 w-7" />
					<span class="text-[15px] font-semibold tracking-tight {isDark ? 'text-white/90' : 'text-zinc-800'}">CashFlow AI</span>
				</a>

				<!-- Desktop Nav -->
				<nav class="hidden items-center gap-0.5 md:flex">
					{#each navLinks as link}
						{@const active = isActive(link.href, $page.url.pathname)}
						{@const stroke = active ? (isDark ? 'rgba(255,255,255,1)' : 'rgba(24,24,27,1)') : (isDark ? 'rgba(255,255,255,0.4)' : 'rgba(113,113,122,1)')}
						<a
							href={link.href}
							class="flex items-center gap-2 rounded-lg px-3 py-2 text-[13px] font-medium transition-all {active ? (isDark ? 'bg-white/[0.06] text-white' : 'bg-zinc-200 text-zinc-900') : (isDark ? 'text-white/40 hover:text-white/70' : 'text-zinc-500 hover:text-zinc-700')}"
						>
							{#if link.href === '/dashboard'}
								<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18" fill="none">
									<path d="M9 16V12.75" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<path d="M3.145 5.95L8.395 1.96C8.753 1.688 9.248 1.688 9.605 1.96L14.855 5.95C15.104 6.139 15.25 6.434 15.25 6.746V14.25C15.25 15.355 14.355 16.25 13.25 16.25H4.75C3.645 16.25 2.75 15.355 2.75 14.25V6.746C2.75 6.433 2.896 6.139 3.145 5.95Z" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								</svg>
							{:else if link.href === '/payments'}
								<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18" fill="none">
									<line x1="1.75" y1="7.25" x2="16.25" y2="7.25" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<rect x="1.75" y="3.75" width="14.5" height="10.5" rx="2" ry="2" transform="translate(18 18) rotate(180)" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<line x1="4.25" y1="11.25" x2="7.25" y2="11.25" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<line x1="12.75" y1="11.25" x2="13.75" y2="11.25" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								</svg>
							{:else if link.href === '/invoices'}
								<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18" fill="none">
									<line x1="5.75" y1="6.75" x2="7.75" y2="6.75" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<line x1="5.75" y1="9.75" x2="12.25" y2="9.75" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<line x1="5.75" y1="12.75" x2="12.25" y2="12.75" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<path d="M2.75,14.25V3.75c0-1.105,.895-2,2-2h5.586c.265,0,.52,.105,.707,.293l3.914,3.914c.188,.188,.293,.442,.293,.707v7.586c0,1.105-.895,2-2,2H4.75c-1.105,0-2-.895-2-2Z" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<path d="M15.16,6.25h-3.41c-.552,0-1-.448-1-1V1.852" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								</svg>
							{:else if link.href === '/imarisha'}
								<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18" fill="none">
									<path d="m12.974,8.731c-.4527,3.525-3.4373,4.0684-6.5358,3.5928" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<path d="m2.75,15.25S4.062,3.729,15.25,2.75c-.56.976-.573,2.605-.946,4.239-.524,2.011-2.335,2.261-4.554,2.261" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								</svg>
							{:else if link.href === '/reports'}
								<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18" fill="none">
									<rect x="13.25" y="2.75" width="2.5" height="12.5" rx="1" ry="1" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<rect x="7.75" y="7.75" width="2.5" height="7.5" rx="1" ry="1" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<rect x="2.25" y="11.75" width="2.5" height="3.5" rx="1" ry="1" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<polyline points="6.25 2.75 8.75 2.75 8.75 5.25" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<line x1="8.5" y1="3" x2="2.75" y2="8.75" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								</svg>
							{/if}
							{link.label}
						</a>
					{/each}
				</nav>

				<!-- Right -->
				<div class="flex items-center gap-1.5">
					{#if $wsConnected}
						<span class="mr-1 h-1.5 w-1.5 rounded-full bg-emerald-400" title="Live"></span>
					{/if}

					<!-- Theme toggle -->
					<button
						onclick={toggleTheme}
						class="flex h-8 w-8 items-center justify-center rounded-lg {isDark ? 'text-white/30' : 'text-zinc-400'} transition-colors {isDark ? 'hover:bg-white/[0.06] hover:text-white/60' : 'hover:bg-zinc-100 hover:text-zinc-600'}"
						title="Toggle theme"
					>
						{#if $theme === 'dark'}
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
							</svg>
						{:else}
							<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />
							</svg>
						{/if}
					</button>

					<NotificationBell />

					<!-- User dropdown -->
					<div class="relative">
						<button
							onclick={() => (userMenuOpen = !userMenuOpen)}
							class="flex items-center gap-2 rounded-lg px-2 py-1.5 transition-colors {isDark ? 'hover:bg-white/[0.06]' : 'hover:bg-zinc-100'}"
						>
							<img src={getAvatarUrl($auth.name || $auth.email || 'user')} alt="Avatar" class="h-7 w-7 rounded-full" />
							<span class="hidden text-[13px] {isDark ? 'text-white/50' : 'text-zinc-500'} sm:inline">{$auth.name}</span>
							<svg xmlns="http://www.w3.org/2000/svg" class="hidden h-3 w-3 {isDark ? 'text-white/20' : 'text-zinc-400'} sm:block" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
								<path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
							</svg>
						</button>

						{#if userMenuOpen}
							<button class="fixed inset-0 z-40" onclick={() => (userMenuOpen = false)} aria-label="Close"></button>
							<div class="absolute right-0 top-full z-50 mt-2 w-56 rounded-xl border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-zinc-900/95' : 'bg-white/95'} p-1.5 shadow-2xl backdrop-blur-xl">
								<div class="border-b {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} px-3 py-3">
									<p class="text-[13px] font-medium {isDark ? 'text-white/80' : 'text-zinc-800'}">{$auth.name}</p>
									{#if $auth.email}
										<p class="mt-0.5 text-[11px] {isDark ? 'text-white/25' : 'text-zinc-400'}">{$auth.email}</p>
									{/if}
								</div>
								<div class="py-1.5">
									<a href="/profile" onclick={() => (userMenuOpen = false)} class="flex items-center gap-2.5 rounded-lg px-3 py-2 text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'} transition-colors {isDark ? 'hover:bg-white/[0.04] hover:text-white/70' : 'hover:bg-zinc-50 hover:text-zinc-700'}">
										<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M17.982 18.725A7.488 7.488 0 0012 15.75a7.488 7.488 0 00-5.982 2.975m11.963 0a9 9 0 10-11.963 0m11.963 0A8.966 8.966 0 0112 21a8.966 8.966 0 01-5.982-2.275M15 9.75a3 3 0 11-6 0 3 3 0 016 0z" /></svg>
										Profile
									</a>
									<a href="/invoices/new" onclick={() => (userMenuOpen = false)} class="flex items-center gap-2.5 rounded-lg px-3 py-2 text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'} transition-colors {isDark ? 'hover:bg-white/[0.04] hover:text-white/70' : 'hover:bg-zinc-50 hover:text-zinc-700'}">
										<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>
										New Invoice
									</a>
								</div>
								<div class="border-t {isDark ? 'border-white/[0.04]' : 'border-zinc-200'} pt-1.5">
									<button onclick={handleLogout} class="flex w-full items-center gap-2.5 rounded-lg px-3 py-2 text-[13px] text-red-400/60 transition-colors hover:bg-red-500/[0.06] hover:text-red-400">
										<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" /></svg>
										Sign out
									</button>
								</div>
							</div>
						{/if}
					</div>

					<!-- Mobile toggle -->
					<button
						onclick={() => (mobileMenuOpen = !mobileMenuOpen)}
						class="flex h-8 w-8 items-center justify-center rounded-lg {isDark ? 'text-white/30' : 'text-zinc-400'} {isDark ? 'hover:bg-white/[0.06]' : 'hover:bg-zinc-100'} md:hidden"
					>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							{#if mobileMenuOpen}
								<path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
							{:else}
								<path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
							{/if}
						</svg>
					</button>
				</div>
			</div>

			<!-- Mobile nav -->
			{#if mobileMenuOpen}
				<div class="mt-2 rounded-2xl border {isDark ? 'border-white/[0.06]' : 'border-zinc-200'} {isDark ? 'bg-zinc-950/90' : 'bg-white/90'} p-2 backdrop-blur-xl md:hidden">
					{#each navLinks as link}
						{@const active = isActive(link.href, $page.url.pathname)}
						{@const stroke = active ? (isDark ? 'rgba(255,255,255,1)' : 'rgba(24,24,27,1)') : (isDark ? 'rgba(255,255,255,0.4)' : 'rgba(113,113,122,1)')}
						<a
							href={link.href}
							onclick={() => (mobileMenuOpen = false)}
							class="flex items-center gap-2.5 rounded-xl px-3 py-3 text-[13px] font-medium transition-all {active ? (isDark ? 'bg-white/[0.06] text-white' : 'bg-zinc-200 text-zinc-900') : (isDark ? 'text-white/40' : 'text-zinc-500')}"
						>
							{#if link.href === '/dashboard'}
								<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18" fill="none">
									<path d="M9 16V12.75" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<path d="M3.145 5.95L8.395 1.96C8.753 1.688 9.248 1.688 9.605 1.96L14.855 5.95C15.104 6.139 15.25 6.434 15.25 6.746V14.25C15.25 15.355 14.355 16.25 13.25 16.25H4.75C3.645 16.25 2.75 15.355 2.75 14.25V6.746C2.75 6.433 2.896 6.139 3.145 5.95Z" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								</svg>
							{:else if link.href === '/payments'}
								<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18" fill="none">
									<line x1="1.75" y1="7.25" x2="16.25" y2="7.25" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<rect x="1.75" y="3.75" width="14.5" height="10.5" rx="2" ry="2" transform="translate(18 18) rotate(180)" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<line x1="4.25" y1="11.25" x2="7.25" y2="11.25" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<line x1="12.75" y1="11.25" x2="13.75" y2="11.25" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								</svg>
							{:else if link.href === '/invoices'}
								<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18" fill="none">
									<line x1="5.75" y1="6.75" x2="7.75" y2="6.75" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<line x1="5.75" y1="9.75" x2="12.25" y2="9.75" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<line x1="5.75" y1="12.75" x2="12.25" y2="12.75" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<path d="M2.75,14.25V3.75c0-1.105,.895-2,2-2h5.586c.265,0,.52,.105,.707,.293l3.914,3.914c.188,.188,.293,.442,.293,.707v7.586c0,1.105-.895,2-2,2H4.75c-1.105,0-2-.895-2-2Z" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<path d="M15.16,6.25h-3.41c-.552,0-1-.448-1-1V1.852" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								</svg>
							{:else if link.href === '/imarisha'}
								<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18" fill="none">
									<path d="m12.974,8.731c-.4527,3.525-3.4373,4.0684-6.5358,3.5928" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<path d="m2.75,15.25S4.062,3.729,15.25,2.75c-.56.976-.573,2.605-.946,4.239-.524,2.011-2.335,2.261-4.554,2.261" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								</svg>
							{:else if link.href === '/reports'}
								<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 18 18" fill="none">
									<rect x="13.25" y="2.75" width="2.5" height="12.5" rx="1" ry="1" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<rect x="7.75" y="7.75" width="2.5" height="7.5" rx="1" ry="1" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<rect x="2.25" y="11.75" width="2.5" height="3.5" rx="1" ry="1" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<polyline points="6.25 2.75 8.75 2.75 8.75 5.25" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
									<line x1="8.5" y1="3" x2="2.75" y2="8.75" stroke={stroke} stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
								</svg>
							{/if}
							{link.label}
						</a>
					{/each}
					<button
						onclick={toggleTheme}
						class="mt-1 flex w-full items-center gap-2.5 rounded-xl px-3 py-3 text-[13px] font-medium {isDark ? 'text-white/40' : 'text-zinc-500'}"
					>
						<svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							{#if $theme === 'dark'}
								<path stroke-linecap="round" stroke-linejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
							{:else}
								<path stroke-linecap="round" stroke-linejoin="round" d="M21.752 15.002A9.718 9.718 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />
							{/if}
						</svg>
						{$theme === 'dark' ? 'Light Mode' : 'Dark Mode'}
					</button>
				</div>
			{/if}
		</div>
	</header>
{/if}

<Toaster />
<div class="{showNav ? (isDark ? 'bg-zinc-950' : 'bg-gray-50') : ''} min-h-screen">
{@render children()}
</div>
