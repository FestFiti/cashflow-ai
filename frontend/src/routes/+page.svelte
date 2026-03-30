<script lang="ts">
	import { theme } from '$lib/stores/theme';
	import { onMount } from 'svelte';

	import LandingNav from '$lib/components/landing/LandingNav.svelte';
	import LandingHero from '$lib/components/landing/LandingHero.svelte';
	import LandingFeatures from '$lib/components/landing/LandingFeatures.svelte';
	import LandingProcess from '$lib/components/landing/LandingProcess.svelte';
	import LandingIntegrations from '$lib/components/landing/LandingIntegrations.svelte';
	import LandingCTA from '$lib/components/landing/LandingCTA.svelte';
	import LandingTechStack from '$lib/components/landing/LandingTechStack.svelte';
	import LandingBuiltBy from '$lib/components/landing/LandingBuiltBy.svelte';
	import LandingFooter from '$lib/components/landing/LandingFooter.svelte';

	const isDark = $derived($theme === 'dark');

	let heroVisible = $state(false);
	let statsVisible = $state(false);
	let featuresVisible = $state(false);
	let techVisible = $state(false);
	let builtByVisible = $state(false);

	onMount(() => {
		setTimeout(() => (heroVisible = true), 100);
		setTimeout(() => (statsVisible = true), 600);

		const observer = new IntersectionObserver(
			(entries) => {
				entries.forEach((entry) => {
					if (entry.target.id === 'features' && entry.isIntersecting) featuresVisible = true;
					if (entry.target.id === 'tech-stack' && entry.isIntersecting) techVisible = true;
					if (entry.target.id === 'built-by' && entry.isIntersecting) builtByVisible = true;
				});
			},
			{ threshold: 0.15 }
		);
		document.querySelectorAll('#features, #tech-stack, #built-by').forEach(el => observer.observe(el));
		return () => observer.disconnect();
	});
</script>

<svelte:head>
	<title>CashFlow AI — Intelligent Business Payment Orchestration</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<LandingNav {isDark} />
<LandingHero {isDark} {heroVisible} {statsVisible} />
<LandingFeatures {isDark} {featuresVisible} />
<LandingProcess {isDark} />
<LandingIntegrations {isDark} />
<LandingCTA {isDark} />
<LandingTechStack {isDark} {techVisible} />
<LandingBuiltBy {isDark} {builtByVisible} />
<LandingFooter {isDark} />

<style>
	@keyframes float-left {
		0%, 100% { transform: translateY(0px) rotate(-1deg); }
		50% { transform: translateY(-12px) rotate(0deg); }
	}
	@keyframes float-right {
		0%, 100% { transform: translateY(0px) rotate(1deg); }
		50% { transform: translateY(-10px) rotate(0deg); }
	}
	@keyframes pulse-dot {
		0%, 100% { opacity: 0.3; transform: scale(1); }
		50% { opacity: 0.8; transform: scale(1.3); }
	}

	:global(.mpesa-grid) {
		animation: grid-drift 20s linear infinite;
	}
	@keyframes grid-drift {
		0% { transform: translate(0, 0); }
		100% { transform: translate(40px, 40px); }
	}

	:global(.ai-dots) {
		animation: dots-rotate 40s linear infinite;
		transform-origin: center center;
	}
	@keyframes dots-rotate {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(0deg); }
	}

	:global(.ratiba-stripes) {
		animation: stripes-slide 12s linear infinite;
	}
	@keyframes stripes-slide {
		0% { transform: translate(0, 0); }
		100% { transform: translate(17px, 17px); }
	}

	:global(.timeline-fill) {
		animation: timeline-sweep 2.4s ease-in-out infinite;
	}
	@keyframes timeline-sweep {
		0% { width: 0%; opacity: 0; }
		40% { width: 100%; opacity: 1; }
		70% { width: 100%; opacity: 0.3; }
		100% { width: 0%; opacity: 0; }
	}

	@keyframes mail-float {
		0%, 100% { transform: translateY(0px); opacity: 0.15; }
		50% { transform: translateY(-10px); opacity: 0.4; }
	}

	@keyframes cursor-blink {
		0%, 100% { opacity: 1; }
		50% { opacity: 0; }
	}

	@keyframes ring-expand {
		0% { transform: translate(-50%, -50%) scale(0.5); opacity: 0.4; }
		100% { transform: translate(-50%, -50%) scale(1.8); opacity: 0; }
	}

	@keyframes bell-ring {
		0%, 80%, 100% { transform: rotate(0deg); }
		5% { transform: rotate(12deg); }
		10% { transform: rotate(-10deg); }
		15% { transform: rotate(8deg); }
		20% { transform: rotate(-5deg); }
		25% { transform: rotate(0deg); }
	}

	@keyframes bar-breathe {
		0%, 100% { transform: scaleY(1); }
		50% { transform: scaleY(1.4); }
	}

	@keyframes bar-grow {
		0% { transform: scaleY(0); opacity: 0; }
		100% { transform: scaleY(1); opacity: 1; }
	}

	:global(.team-dots) {
		animation: grid-drift 25s linear infinite reverse;
	}
</style>
