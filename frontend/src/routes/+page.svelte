<script lang="ts">
	import { auth } from '$lib/stores/auth';
</script>

<svelte:head>
	<title>CashFlow AI — Intelligent Business Payment Orchestration</title>
</svelte:head>

<!-- Hero Section -->
<section class="relative min-h-screen overflow-hidden">
	<!-- Background gradients -->
	<div class="pointer-events-none absolute inset-0">
		<div class="absolute -left-40 top-20 h-96 w-96 rounded-full bg-emerald-500/10 blur-3xl"></div>
		<div class="absolute -right-40 top-60 h-96 w-96 rounded-full bg-blue-500/10 blur-3xl"></div>
	</div>

	<div class="relative mx-auto max-w-7xl px-4 pb-20 pt-24 md:px-8 md:pt-32">
		<!-- Status badge -->
		<div class="animate-fade-in-up mb-8 flex justify-center">
			<div
				class="inline-flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-4 py-1.5"
			>
				<span class="h-2 w-2 animate-pulse rounded-full bg-emerald-400"></span>
				<span class="text-sm font-medium text-emerald-400"
					>AI-Powered Cash Flow Management</span
				>
			</div>
		</div>

		<!-- Heading -->
		<h1
			class="animate-fade-in-up mx-auto max-w-4xl text-center text-5xl font-black leading-tight tracking-tighter md:text-7xl lg:text-8xl"
		>
			Never miss a
			<span
				class="bg-gradient-to-r from-emerald-400 to-emerald-600 bg-clip-text text-transparent"
			>
				payment
			</span>
			again
		</h1>

		<p
			class="animate-fade-in-up animation-delay-100 mx-auto mt-6 max-w-2xl text-center text-lg text-zinc-400 md:text-xl"
		>
			Automate invoicing, collect via M-Pesa, and let AI handle your reminders.
			Built for African businesses that move fast.
		</p>

		<!-- CTA buttons -->
		<div
			class="animate-fade-in-up animation-delay-200 mt-10 flex flex-col items-center justify-center gap-4 sm:flex-row"
		>
			<a
				href={$auth.token ? '/dashboard' : '/register'}
				class="gradient-bg-emerald inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-8 py-3.5 text-base font-semibold text-white transition-all hover:bg-emerald-500 hover:shadow-lg hover:shadow-emerald-500/25"
			>
				Get Started Free
				<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
					<path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
				</svg>
			</a>
			<a
				href="#how-it-works"
				class="inline-flex items-center gap-2 rounded-xl border border-zinc-700 px-8 py-3.5 text-base font-semibold text-zinc-300 transition-all hover:border-zinc-500 hover:bg-zinc-800/50"
			>
				See How It Works
			</a>
		</div>

		<!-- Floating preview cards -->
		<div class="animate-fade-in-up animation-delay-300 mt-16 hidden md:block">
			<div class="mx-auto grid max-w-4xl grid-cols-3 gap-4">
				<div
					class="gradient-bg rounded-[20px] border border-zinc-800 bg-zinc-900/50 p-5 backdrop-blur-sm"
				>
					<div class="mb-3 flex items-center gap-2">
						<div class="h-3 w-3 rounded-full bg-emerald-400"></div>
						<span class="text-xs font-medium uppercase tracking-widest text-zinc-500"
							>Invoice Sent</span
						>
					</div>
					<p class="text-2xl font-bold">KES 12,000</p>
					<p class="mt-1 text-sm text-zinc-500">John Kamau — Web Design</p>
				</div>
				<div
					class="gradient-bg-emerald rounded-[20px] border border-emerald-500/20 bg-emerald-500/5 p-5 backdrop-blur-sm"
				>
					<div class="mb-3 flex items-center gap-2">
						<div class="h-3 w-3 rounded-full bg-emerald-400 animate-pulse-slow"></div>
						<span class="text-xs font-medium uppercase tracking-widest text-emerald-500"
							>Payment Received</span
						>
					</div>
					<p class="text-2xl font-bold text-emerald-400">KES 45,000</p>
					<p class="mt-1 text-sm text-zinc-500">M-Pesa confirmed</p>
				</div>
				<div
					class="gradient-bg rounded-[20px] border border-zinc-800 bg-zinc-900/50 p-5 backdrop-blur-sm"
				>
					<div class="mb-3 flex items-center gap-2">
						<div class="h-3 w-3 rounded-full bg-blue-400"></div>
						<span class="text-xs font-medium uppercase tracking-widest text-zinc-500"
							>AI Reminder</span
						>
					</div>
					<p class="text-sm text-zinc-300">"Hi John, a reminder about your invoice..."</p>
					<p class="mt-2 text-xs text-zinc-600">Scheduled: 2 days before due</p>
				</div>
			</div>
		</div>
	</div>
</section>

<!-- Stats Bar -->
<section class="border-y border-zinc-800 bg-zinc-900/30">
	<div class="mx-auto grid max-w-5xl grid-cols-2 gap-6 px-4 py-10 md:grid-cols-4 md:px-8">
		{#each [
			{ value: '10K+', label: 'Invoices Generated' },
			{ value: 'KES 50M+', label: 'Payments Tracked' },
			{ value: '95%', label: 'Collection Rate' },
			{ value: '5K+', label: 'Businesses' }
		] as stat, i}
			<div class="animate-fade-in-up text-center" style="animation-delay: {i * 0.1}s">
				<p class="text-3xl font-black tracking-tight">{stat.value}</p>
				<p class="mt-1 text-sm text-zinc-500">{stat.label}</p>
			</div>
		{/each}
	</div>
</section>

<!-- Features Section -->
<section id="features" class="py-20">
	<div class="mx-auto max-w-7xl px-4 md:px-8">
		<h2 class="mb-4 text-center text-3xl font-bold tracking-tight md:text-4xl">
			Everything you need to
			<span class="bg-gradient-to-r from-emerald-400 to-emerald-600 bg-clip-text text-transparent">
				get paid
			</span>
		</h2>
		<p class="mx-auto mb-12 max-w-2xl text-center text-zinc-500">
			From AI invoice generation to automated M-Pesa collection — one platform for your entire cash flow.
		</p>

		<div class="grid grid-cols-1 gap-6 md:grid-cols-3">
			{#each [
				{
					icon: '\u{2728}',
					title: 'AI Invoice Generation',
					description: 'Describe a transaction in plain language. Claude AI generates a professional invoice instantly.',
					color: 'emerald'
				},
				{
					icon: '\u{1F4F1}',
					title: 'M-Pesa Integration',
					description: 'STK Push payment links, B2C disbursements, and real-time payment confirmations.',
					color: 'blue'
				},
				{
					icon: '\u{23F0}',
					title: 'Smart Reminders',
					description: 'AI determines optimal timing and drafts personalised SMS reminders via Ratiba.',
					color: 'amber'
				}
			] as feature}
				<div
					class="gradient-bg rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-6 transition-all hover:border-zinc-700"
				>
					<div
						class="mb-4 flex h-12 w-12 items-center justify-center rounded-xl text-2xl {feature.color === 'emerald' ? 'bg-emerald-900' : feature.color === 'blue' ? 'bg-blue-900' : 'bg-amber-900'}"
					>
						{feature.icon}
					</div>
					<h3 class="mb-2 text-lg font-semibold">{feature.title}</h3>
					<p class="text-sm leading-relaxed text-zinc-400">{feature.description}</p>
				</div>
			{/each}
		</div>
	</div>
</section>

<!-- How It Works -->
<section id="how-it-works" class="border-t border-zinc-800 py-20">
	<div class="mx-auto max-w-5xl px-4 md:px-8">
		<h2 class="mb-12 text-center text-3xl font-bold tracking-tight md:text-4xl">
			How it works
		</h2>

		<div class="grid grid-cols-1 gap-8 md:grid-cols-3">
			{#each [
				{ step: '01', title: 'Create an Invoice', desc: 'Type a description or let AI generate it. Attach an M-Pesa payment link automatically.' },
				{ step: '02', title: 'Send & Schedule', desc: 'Send the invoice to your client. Ratiba schedules smart reminders before and on the due date.' },
				{ step: '03', title: 'Get Paid', desc: 'Client pays via M-Pesa STK Push. Invoice status updates in real time on your dashboard.' }
			] as item}
				<div class="relative rounded-[20px] border border-zinc-800 bg-zinc-900/30 p-6">
					<span class="absolute -top-4 right-4 text-5xl font-black text-zinc-800/50">
						{item.step}
					</span>
					<h3 class="mb-2 text-lg font-semibold">{item.title}</h3>
					<p class="text-sm leading-relaxed text-zinc-400">{item.desc}</p>
				</div>
			{/each}
		</div>
	</div>
</section>

<!-- CTA Block -->
<section class="py-20">
	<div class="mx-auto max-w-4xl px-4 md:px-8">
		<div
			class="gradient-bg-emerald overflow-hidden rounded-[24px] border border-emerald-500/20 bg-emerald-500/5 p-8 text-center md:p-12"
		>
			<h2 class="mb-4 text-3xl font-bold tracking-tight md:text-4xl">
				Ready to automate your cash flow?
			</h2>
			<p class="mx-auto mb-8 max-w-xl text-zinc-400">
				Join thousands of African businesses using CashFlow AI to get paid faster, track every shilling, and never chase a payment manually again.
			</p>
			<a
				href="/register"
				class="inline-flex items-center gap-2 rounded-xl bg-emerald-600 px-8 py-3.5 text-base font-semibold text-white transition-all hover:bg-emerald-500 hover:shadow-lg hover:shadow-emerald-500/25"
			>
				Start for Free
				<svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
					<path fill-rule="evenodd" d="M10.293 3.293a1 1 0 011.414 0l6 6a1 1 0 010 1.414l-6 6a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-4.293-4.293a1 1 0 010-1.414z" clip-rule="evenodd" />
				</svg>
			</a>
		</div>
	</div>
</section>
