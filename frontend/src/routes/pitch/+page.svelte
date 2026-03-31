<script lang="ts">
	import { onMount } from 'svelte';
	import 'reveal.js/reveal.css';

	let revealEl: HTMLDivElement;
	let deck: any;
	let qrApp = $state('');
	let qrDemo = $state('');

	onMount(async () => {
		const [Reveal, QRCode] = await Promise.all([
			import('reveal.js').then(m => m.default),
			import('qrcode').then(m => m.default),
		]);
		const qrOpts = { width: 220, margin: 2, errorCorrectionLevel: 'M' as const, color: { dark: '#10b981', light: '#00000000' } };
		qrApp = await QRCode.toDataURL('https://flowai.cash', qrOpts);
		qrDemo = await QRCode.toDataURL('https://flowai.cash/demo', { ...qrOpts, color: { dark: '#ffffff', light: '#00000000' } });
		deck = new Reveal(revealEl, {
			hash: true,
			controls: true,
			progress: true,
			center: true,
			transition: 'slide',
			autoAnimateDuration: 0.8,
			autoAnimateEasing: 'ease',
			width: 1440,
			height: 810,
			margin: 0.04,
			disableLayout: false,
			embedded: false,
			minScale: 0.1,
			maxScale: 5.0,
			backgroundTransition: 'fade',
		});
		deck.initialize();

		// Auto-advance fragments within a slide (400ms between each)
		let fragmentTimer: ReturnType<typeof setInterval> | null = null;
		function startFragments() {
			stopFragments();
			fragmentTimer = setInterval(() => {
				if (deck.availableFragments().next) {
					deck.nextFragment();
				} else {
					stopFragments();
				}
			}, 400);
		}
		function stopFragments() {
			if (fragmentTimer) { clearInterval(fragmentTimer); fragmentTimer = null; }
		}
		deck.on('slidechanged', () => { startFragments(); });
		deck.on('ready', () => { startFragments(); });

		// Allow browser zoom (Ctrl+/-)
		deck.configure({ keyboard: { 187: null, 189: null, 48: null } });
	});
</script>

<svelte:head>
	<title>CashFlow AI — Pitch Deck</title>
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin="anonymous" />
	<link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet" />
</svelte:head>

<div class="reveal" bind:this={revealEl}>
	<div class="slides">

		<!-- ==================== WELCOME / QR ==================== -->
		<section data-background-color="#09090b">
			<div class="flex flex-col items-center justify-center gap-6">
				<img src="/logo-gold.png" alt="CashFlow AI" class="w-16 h-16 mb-2" />
				<h2 class="font-serif text-5xl text-white">
					Welcome to <span class="italic text-emerald-400">Demo Day</span>
				</h2>
				<p class="text-xl text-white/40 mb-4">Scan to follow along on your phone</p>
				<div class="flex items-start gap-16">
					<div class="text-center">
						{#if qrApp}
							<img src={qrApp} alt="QR App" class="mx-auto h-48 w-48 mb-4" />
						{/if}
						<p class="text-lg text-emerald-400 font-medium">flowai.cash</p>
						<p class="text-sm text-white/30 mt-1">Try the live app</p>
					</div>
					<div class="text-center">
						{#if qrDemo}
							<img src={qrDemo} alt="QR Demo Page" class="mx-auto h-48 w-48 mb-4" />
						{/if}
						<p class="text-lg text-white font-medium">flowai.cash/demo</p>
						<p class="text-sm text-white/30 mt-1">Instructions + QR codes</p>
					</div>
				</div>
				<p class="mt-6 text-base text-white/20">We'll begin shortly — feel free to explore</p>
			</div>
		</section>

		<!-- ==================== TITLE ==================== -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="flex flex-col items-center justify-center gap-8">
				<img src="/logo-gold.png" alt="CashFlow AI" class="w-24 h-24" data-id="logo" />
				<h1 class="font-serif text-7xl tracking-tight text-white" data-id="title">
					Cash<span class="text-emerald-400 italic">Flow</span> AI
				</h1>
				<p class="text-2xl text-white/40 font-light tracking-wide">Intelligent Payment Orchestration for Africa</p>
				<div class="mt-8 flex items-center gap-3">
					<span class="inline-flex items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-5 py-2 text-sm text-emerald-400">
						<span class="relative flex h-2 w-2"><span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span><span class="relative inline-flex h-2 w-2 rounded-full bg-emerald-400"></span></span>
						Money in Motion Demo Day
					</span>
				</div>
				<p class="text-lg text-white/20 mt-4">31st March 2026 &middot; Nairobi</p>
			</div>
		</section>

		<!-- ==================== ELEVATOR PITCH ==================== -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 mb-6 font-medium">The Pitch</p>
				<h2 class="font-serif text-5xl leading-tight text-white mb-12" data-id="title">
					In <span class="text-emerald-400 italic">30 seconds</span>
				</h2>
				<blockquote class="fragment fade-up border-l-4 border-emerald-500 pl-8 text-2xl leading-relaxed text-white/70">
					We help <strong class="text-white">African freelancers and small businesses</strong> who struggle with
					<strong class="text-white">getting paid on time</strong> by offering
					<strong class="text-emerald-400">an AI-powered invoicing platform with built-in M-Pesa payments</strong>.
					<br/><br/>
					Unlike QuickBooks or Stripe, our solution is <strong class="text-white">built natively for M-Pesa</strong> — the way 96% of Kenyans actually pay.
				</blockquote>
			</div>
		</section>

		<!-- ==================== THE PROBLEM ==================== -->
		<section data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 mb-6 font-medium">The Problem</p>
				<h2 class="font-serif text-6xl text-white mb-6">
					African SMEs are <span class="text-red-400 italic">bleeding money</span><br/>they've already earned.
				</h2>
			</div>
		</section>

		<section data-auto-animate data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 mb-6 font-medium">The Problem</p>
				<div class="grid grid-cols-2 gap-8" data-id="stats">
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-10" data-fragment-index="0">
						<p class="font-serif text-8xl text-red-400 italic">60%</p>
						<p class="mt-4 text-xl text-white/50">of SMEs wait <strong class="text-white">45-60 days</strong> to get paid</p>
					</div>
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-10" data-fragment-index="1">
						<p class="font-serif text-8xl text-amber-400 italic">70%</p>
						<p class="mt-4 text-xl text-white/50">still invoice <strong class="text-white">manually</strong> — 15-20 hrs/week</p>
					</div>
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-10" data-fragment-index="2">
						<p class="font-serif text-8xl text-orange-400 italic">8-12%</p>
						<p class="mt-4 text-xl text-white/50">of annual revenue <strong class="text-white">lost</strong> to payment delays</p>
					</div>
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-10" data-fragment-index="3">
						<p class="font-serif text-8xl text-rose-400 italic">40%</p>
						<p class="mt-4 text-xl text-white/50"><strong class="text-white">cannot scale</strong> — cash stuck in receivables</p>
					</div>
				</div>
			</div>
		</section>

		<section data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 mb-6 font-medium">The Real Workflow Today</p>
				<h2 class="font-serif text-5xl text-white mb-14">The <span class="italic text-amber-400">painful</span> cycle</h2>
				<div class="grid grid-cols-4 gap-6">
					<!-- Step 1 -->
					<div class="fragment fade-right group relative" data-fragment-index="0">
						<div class="pointer-events-none absolute -inset-3 opacity-20">
							<div class="absolute top-[8px] -left-[12px] h-[1px] w-[calc(100%+24px)] bg-amber-500/60"></div>
							<div class="absolute bottom-[8px] -right-[12px] h-[1px] w-[calc(100%+24px)] bg-amber-500/60"></div>
							<div class="absolute -top-[12px] left-[8px] h-[calc(100%+24px)] w-[1px] bg-amber-500/60"></div>
							<div class="absolute -bottom-[12px] right-[8px] h-[calc(100%+24px)] w-[1px] bg-amber-500/60"></div>
						</div>
						<div class="relative rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8 text-center h-full flex flex-col items-center justify-center">
							<span class="flex h-12 w-12 items-center justify-center rounded-full border border-amber-500/20 bg-amber-500/[0.08] mb-5">
								<p class="text-2xl font-bold text-amber-400">1</p>
							</span>
							<p class="text-xl text-white/80 font-medium mb-2">Send invoice</p>
							<p class="text-sm text-white/30">WhatsApp PDF or verbal</p>
						</div>
					</div>
					<!-- Step 2 -->
					<div class="fragment fade-right group relative" data-fragment-index="1">
						<div class="pointer-events-none absolute -inset-3 opacity-20">
							<div class="absolute top-[8px] -left-[12px] h-[1px] w-[calc(100%+24px)] bg-amber-500/60"></div>
							<div class="absolute bottom-[8px] -right-[12px] h-[1px] w-[calc(100%+24px)] bg-amber-500/60"></div>
							<div class="absolute -top-[12px] left-[8px] h-[calc(100%+24px)] w-[1px] bg-amber-500/60"></div>
							<div class="absolute -bottom-[12px] right-[8px] h-[calc(100%+24px)] w-[1px] bg-amber-500/60"></div>
						</div>
						<div class="relative rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8 text-center h-full flex flex-col items-center justify-center">
							<span class="flex h-12 w-12 items-center justify-center rounded-full border border-orange-500/20 bg-orange-500/[0.08] mb-5">
								<p class="text-2xl font-bold text-orange-400">2</p>
							</span>
							<p class="text-xl text-white/80 font-medium mb-2">Wait. Chase.</p>
							<p class="text-sm text-white/30">Call. Text. Hope.</p>
						</div>
					</div>
					<!-- Step 3 -->
					<div class="fragment fade-right group relative" data-fragment-index="2">
						<div class="pointer-events-none absolute -inset-3 opacity-20">
							<div class="absolute top-[8px] -left-[12px] h-[1px] w-[calc(100%+24px)] bg-orange-500/60"></div>
							<div class="absolute bottom-[8px] -right-[12px] h-[1px] w-[calc(100%+24px)] bg-orange-500/60"></div>
							<div class="absolute -top-[12px] left-[8px] h-[calc(100%+24px)] w-[1px] bg-orange-500/60"></div>
							<div class="absolute -bottom-[12px] right-[8px] h-[calc(100%+24px)] w-[1px] bg-orange-500/60"></div>
						</div>
						<div class="relative rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8 text-center h-full flex flex-col items-center justify-center">
							<span class="flex h-12 w-12 items-center justify-center rounded-full border border-rose-500/20 bg-rose-500/[0.08] mb-5">
								<p class="text-2xl font-bold text-rose-400">3</p>
							</span>
							<p class="text-xl text-white/80 font-medium mb-2">Money arrives</p>
							<p class="text-sm text-white/30">No record. No match.</p>
						</div>
					</div>
					<!-- Step 4 -->
					<div class="fragment fade-right group relative" data-fragment-index="3">
						<div class="pointer-events-none absolute -inset-3 opacity-30">
							<div class="absolute top-[8px] -left-[12px] h-[1px] w-[calc(100%+24px)] bg-red-500/80"></div>
							<div class="absolute bottom-[8px] -right-[12px] h-[1px] w-[calc(100%+24px)] bg-red-500/80"></div>
							<div class="absolute -top-[12px] left-[8px] h-[calc(100%+24px)] w-[1px] bg-red-500/80"></div>
							<div class="absolute -bottom-[12px] right-[8px] h-[calc(100%+24px)] w-[1px] bg-red-500/80"></div>
						</div>
						<div class="relative rounded-2xl border border-red-500/20 bg-red-500/[0.05] p-8 text-center h-full flex flex-col items-center justify-center">
							<span class="flex h-12 w-12 items-center justify-center rounded-full border border-red-500/30 bg-red-500/[0.12] mb-5">
								<p class="text-2xl font-bold text-red-400">4</p>
							</span>
							<p class="text-xl text-red-400/90 font-medium mb-2">Month end</p>
							<p class="text-sm text-red-400/40">No idea what's owed</p>
						</div>
					</div>
				</div>
			</div>
		</section>

		<!-- ==================== THE SOLUTION ==================== -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="flex flex-col items-center justify-center">
				<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 mb-6 font-medium">The Solution</p>
				<h2 class="font-serif text-7xl text-white" data-id="sol">
					Describe what you sold.<br/><span class="text-emerald-400 italic">We handle the rest.</span>
				</h2>
			</div>
		</section>

		<!-- Step 1: Create -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<div class="flex items-center gap-4 mb-8">
					<span class="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500 text-black font-bold text-lg">1</span>
					<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 font-medium">Create with AI</p>
				</div>
				<h2 class="font-serif text-5xl text-white mb-10">Type it in <span class="italic text-emerald-400">plain English</span></h2>
				<div class="fragment fade-up rounded-2xl border border-white/[0.08] bg-white/[0.03] p-8">
					<p class="text-white/30 text-lg mb-4 font-mono">Prompt:</p>
					<p class="text-3xl text-white/80 leading-relaxed font-mono">
						"Invoice John Kamau for <span class="text-emerald-400">3 hours</span> of web design at <span class="text-emerald-400">5,000/hr</span>, due in <span class="text-emerald-400">2 weeks</span>"
					</p>
				</div>
				<div class="fragment fade-up mt-6 flex items-center gap-3">
					<svg class="w-6 h-6 text-emerald-400 animate-pulse" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z"/></svg>
					<p class="text-xl text-white/40">AI parses into professional invoice with line items, totals, and due date</p>
				</div>
			</div>
		</section>

		<!-- Step 2: Send -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<div class="flex items-center gap-4 mb-8">
					<span class="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500 text-black font-bold text-lg">2</span>
					<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 font-medium">Send</p>
				</div>
				<h2 class="font-serif text-5xl text-white mb-10">Email + <span class="italic text-emerald-400">WhatsApp</span> + Payment Link</h2>
				<div class="grid grid-cols-3 gap-6">
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8 text-center" data-fragment-index="0">
						<svg class="w-10 h-10 text-blue-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75"/></svg>
						<p class="text-xl text-white/70 font-medium">Branded Email</p>
						<p class="mt-2 text-sm text-white/30">Professional template with logo</p>
					</div>
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8 text-center" data-fragment-index="1">
						<svg class="w-10 h-10 text-green-400 mx-auto mb-4" viewBox="0 0 24 24" fill="currentColor"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z"/></svg>
						<p class="text-xl text-white/70 font-medium">WhatsApp</p>
						<p class="mt-2 text-sm text-white/30">One tap, pre-filled message</p>
					</div>
					<div class="fragment fade-up rounded-2xl border border-emerald-500/20 bg-emerald-500/[0.05] p-8 text-center" data-fragment-index="2">
						<svg class="w-10 h-10 text-emerald-400 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M13.19 8.688a4.5 4.5 0 011.242 7.244l-4.5 4.5a4.5 4.5 0 01-6.364-6.364l1.757-1.757m9.86-1.06a4.5 4.5 0 00-1.242-7.244l-4.5-4.5a4.5 4.5 0 00-6.364 6.364l1.757 1.757"/></svg>
						<p class="text-xl text-emerald-400 font-medium">Public Pay Link</p>
						<p class="mt-2 text-sm text-emerald-400/40">No signup needed from client</p>
					</div>
				</div>
			</div>
		</section>

		<!-- Step 3: Pay -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<div class="flex items-center gap-4 mb-8">
					<span class="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500 text-black font-bold text-lg">3</span>
					<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 font-medium">Pay via M-Pesa</p>
				</div>
				<h2 class="font-serif text-5xl text-white mb-10">STK Push. <span class="italic text-emerald-400">Enter PIN. Done.</span></h2>
				<div class="flex items-center gap-12">
					<div class="flex-1 space-y-6">
						<div class="flex items-start gap-4">
							<span class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-white/[0.06] text-sm text-white/60">1</span>
							<p class="text-2xl text-white/60">Client opens payment link</p>
						</div>
						<div class="flex items-start gap-4">
							<span class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-white/[0.06] text-sm text-white/60">2</span>
							<p class="text-2xl text-white/60">Enters phone number, taps <strong class="text-white">"Pay"</strong></p>
						</div>
						<div class="flex items-start gap-4">
							<span class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-emerald-500/20 text-sm text-emerald-400">3</span>
							<p class="text-2xl text-white/60">M-Pesa prompt on their phone — <strong class="text-emerald-400">enter PIN</strong></p>
						</div>
						<div class="flex items-start gap-4">
							<span class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-emerald-500 text-sm text-black font-bold">4</span>
							<p class="text-2xl text-white"><strong>Payment confirmed in seconds</strong></p>
						</div>
					</div>
					<div class="fragment grow flex-shrink-0 rounded-2xl border border-emerald-500/20 bg-emerald-500/[0.03] p-10 text-center" data-fragment-index="4">
						<p class="text-lg text-emerald-400/60 mb-2">No bank details</p>
						<p class="text-lg text-emerald-400/60 mb-2">No card numbers</p>
						<p class="text-lg text-emerald-400/60 mb-4">No app download</p>
						<p class="font-serif text-4xl text-emerald-400 italic">Zero friction</p>
					</div>
				</div>
			</div>
		</section>

		<!-- Step 4: Track -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<div class="flex items-center gap-4 mb-8">
					<span class="flex h-10 w-10 items-center justify-center rounded-full bg-emerald-500 text-black font-bold text-lg">4</span>
					<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 font-medium">Real-Time Tracking</p>
				</div>
				<h2 class="font-serif text-5xl text-white mb-10">Dashboard updates <span class="italic text-emerald-400">instantly</span></h2>
				<div class="grid grid-cols-4 gap-4">
					<div class="fragment fade-up rounded-2xl border border-emerald-500/20 bg-emerald-500/[0.03] p-6" data-fragment-index="0">
						<p class="text-sm text-emerald-400/60 uppercase tracking-wider mb-2">Receivables</p>
						<p class="font-serif text-4xl text-emerald-400 italic">KES 248K</p>
					</div>
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6" data-fragment-index="1">
						<p class="text-sm text-white/30 uppercase tracking-wider mb-2">Collected</p>
						<p class="font-serif text-4xl text-white italic">KES 185K</p>
					</div>
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6" data-fragment-index="2">
						<p class="text-sm text-white/30 uppercase tracking-wider mb-2">Collection Rate</p>
						<p class="font-serif text-4xl text-white italic">96%</p>
					</div>
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-6" data-fragment-index="3">
						<p class="text-sm text-white/30 uppercase tracking-wider mb-2">Overdue</p>
						<p class="font-serif text-4xl text-amber-400 italic">2</p>
					</div>
				</div>
				<div class="fragment fade-in mt-8 flex items-center gap-3 text-white/40 text-lg">
					<span class="relative flex h-3 w-3"><span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span><span class="relative inline-flex h-3 w-3 rounded-full bg-emerald-400"></span></span>
					WebSocket-powered &middot; Invoice marked paid &middot; Receipt emailed &middot; Notification sent
				</div>
			</div>
		</section>

		<!-- ==================== M-PESA ==================== -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 mb-6 font-medium">Why M-Pesa</p>
				<h2 class="font-serif text-6xl text-white mb-12" data-id="mpesa">
					<span class="text-emerald-400 italic">96%</span> of Kenyan adults<br/>use mobile money.
				</h2>
				<div class="grid grid-cols-3 gap-6">
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8" data-fragment-index="0">
						<p class="font-serif text-5xl text-white italic mb-3">KES 35T</p>
						<p class="text-lg text-white/40">processed annually via M-Pesa</p>
					</div>
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8" data-fragment-index="1">
						<p class="text-lg text-white/40 mb-6">Stripe, PayPal, and global tools don't support STK Push.</p>
						<p class="text-lg text-white/70 font-medium">We do. Natively.</p>
					</div>
					<div class="fragment fade-up rounded-2xl border border-emerald-500/20 bg-emerald-500/[0.03] p-8" data-fragment-index="2">
						<p class="text-lg text-emerald-400/60 mb-4">Our M-Pesa stack:</p>
						<ul class="space-y-2 text-base text-emerald-400/80">
							<li>STK Push (Lipa Na M-Pesa)</li>
							<li>OAuth token caching (Redis)</li>
							<li>Webhook callbacks</li>
							<li>Auto-reconciliation</li>
							<li>Live environment</li>
						</ul>
					</div>
				</div>
			</div>
		</section>

		<!-- ==================== COMPETITIVE ADVANTAGE ==================== -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 mb-6 font-medium">Competitive Advantage</p>
				<h2 class="font-serif text-5xl text-white mb-12">Built <span class="italic text-emerald-400">for</span> Africa. Not adapted.</h2>
				<div class="grid grid-cols-2 gap-1">
					<div class="fragment fade-right rounded-tl-2xl bg-emerald-500/10 p-6 border-b border-r border-emerald-500/10">
						<p class="text-base text-emerald-400 font-medium mb-1">CashFlow AI</p>
						<p class="text-lg text-white/60">M-Pesa STK Push built-in</p>
					</div>
					<div class="fragment fade-left rounded-tr-2xl bg-white/[0.02] p-6 border-b border-white/[0.04]">
						<p class="text-base text-white/30 font-medium mb-1">Others</p>
						<p class="text-lg text-white/40">Manual bank transfer / cards</p>
					</div>
					<div class="fragment fade-right bg-emerald-500/10 p-6 border-b border-r border-emerald-500/10">
						<p class="text-lg text-white/60">AI invoice from natural language</p>
					</div>
					<div class="fragment fade-left bg-white/[0.02] p-6 border-b border-white/[0.04]">
						<p class="text-lg text-white/40">Form-based creation</p>
					</div>
					<div class="fragment fade-right bg-emerald-500/10 p-6 border-b border-r border-emerald-500/10">
						<p class="text-lg text-white/60">Public payment links (no client signup)</p>
					</div>
					<div class="fragment fade-left bg-white/[0.02] p-6 border-b border-white/[0.04]">
						<p class="text-lg text-white/40">Both parties need accounts</p>
					</div>
					<div class="fragment fade-right bg-emerald-500/10 p-6 border-b border-r border-emerald-500/10">
						<p class="text-lg text-white/60">Real-time WebSocket updates</p>
					</div>
					<div class="fragment fade-left bg-white/[0.02] p-6 border-b border-white/[0.04]">
						<p class="text-lg text-white/40">Refresh to check</p>
					</div>
					<div class="fragment fade-right rounded-bl-2xl bg-emerald-500/10 p-6 border-r border-emerald-500/10">
						<p class="text-lg text-white/60">AI reminders + WhatsApp sharing</p>
					</div>
					<div class="fragment fade-left rounded-br-2xl bg-white/[0.02] p-6">
						<p class="text-lg text-white/40">Separate tools needed</p>
					</div>
				</div>
			</div>
		</section>

		<!-- ==================== BUSINESS MODEL ==================== -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 mb-6 font-medium">Business Model</p>
				<h2 class="font-serif text-5xl text-white mb-12">We make money when <span class="italic text-emerald-400">you make money</span></h2>
				<div class="grid grid-cols-3 gap-6">
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8" data-fragment-index="0">
						<p class="text-sm uppercase tracking-wider text-white/30 mb-4">Transaction Fee</p>
						<p class="font-serif text-5xl text-white italic">0.5-1%</p>
						<p class="mt-3 text-base text-white/40">per M-Pesa payment collected</p>
					</div>
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8" data-fragment-index="1">
						<p class="text-sm uppercase tracking-wider text-white/30 mb-4">Pro Plan</p>
						<p class="font-serif text-5xl text-emerald-400 italic">KES 1.5K</p>
						<p class="mt-3 text-base text-white/40">per month &middot; Unlimited invoices, AI, reports</p>
					</div>
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8" data-fragment-index="2">
						<p class="text-sm uppercase tracking-wider text-white/30 mb-4">Business Plan</p>
						<p class="font-serif text-5xl text-emerald-400 italic">KES 5K</p>
						<p class="mt-3 text-base text-white/40">per month &middot; API, white-label, analytics</p>
					</div>
				</div>
			</div>
		</section>

		<!-- ==================== MARKET ==================== -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 mb-6 font-medium">Market Opportunity</p>
				<h2 class="font-serif text-5xl text-white mb-12">A <span class="italic text-emerald-400">$8.7 billion</span> opportunity</h2>
				<div class="grid grid-cols-3 gap-6">
					<div class="fragment fade-up rounded-2xl border border-emerald-500/20 bg-emerald-500/[0.03] p-8 text-center" data-fragment-index="0">
						<p class="font-serif text-6xl text-emerald-400 italic mb-3">$2.3B</p>
						<p class="text-xl text-white/50">Kenya</p>
						<p class="mt-2 text-sm text-white/30">1.5M SMEs &middot; 7.4M informal workers</p>
					</div>
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8 text-center" data-fragment-index="1">
						<p class="font-serif text-6xl text-white italic mb-3">$8.7B</p>
						<p class="text-xl text-white/50">East Africa</p>
						<p class="mt-2 text-sm text-white/30">Tanzania &middot; Uganda &middot; Rwanda</p>
					</div>
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8 text-center" data-fragment-index="2">
						<p class="font-serif text-6xl text-white/40 italic mb-3">$30B+</p>
						<p class="text-xl text-white/50">Sub-Saharan Africa</p>
						<p class="mt-2 text-sm text-white/30">Nigeria &middot; Ghana &middot; South Africa</p>
					</div>
				</div>
			</div>
		</section>

		<!-- Why Now -->
		<section data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 mb-6 font-medium">Timing</p>
				<h2 class="font-serif text-5xl text-white mb-12">Why <span class="italic text-emerald-400">now?</span></h2>
				<div class="grid grid-cols-2 gap-x-12 gap-y-8">
					<div class="fragment fade-up flex items-start gap-4" data-fragment-index="0">
						<span class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-emerald-500/20 text-emerald-400 text-sm font-bold">1</span>
						<div>
							<p class="text-xl text-white/80 font-medium">Daraja API is mature</p>
							<p class="text-base text-white/40">Reliable STK Push, webhooks, developer self-service</p>
						</div>
					</div>
					<div class="fragment fade-up flex items-start gap-4" data-fragment-index="1">
						<span class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-emerald-500/20 text-emerald-400 text-sm font-bold">2</span>
						<div>
							<p class="text-xl text-white/80 font-medium">AI costs dropped 90%</p>
							<p class="text-base text-white/40">NLP invoice generation is now viable at scale</p>
						</div>
					</div>
					<div class="fragment fade-up flex items-start gap-4" data-fragment-index="2">
						<span class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-emerald-500/20 text-emerald-400 text-sm font-bold">3</span>
						<div>
							<p class="text-xl text-white/80 font-medium">60%+ smartphone penetration</p>
							<p class="text-base text-white/40">Web platform reaches majority of SME owners</p>
						</div>
					</div>
					<div class="fragment fade-up flex items-start gap-4" data-fragment-index="3">
						<span class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-emerald-500/20 text-emerald-400 text-sm font-bold">4</span>
						<div>
							<p class="text-xl text-white/80 font-medium">Post-COVID digital shift</p>
							<p class="text-base text-white/40">SMEs actively seeking digital financial tools</p>
						</div>
					</div>
				</div>
			</div>
		</section>

		<!-- ==================== TECH STACK ==================== -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 mb-6 font-medium">Architecture</p>
				<h2 class="font-serif text-5xl text-white mb-12">What's under the <span class="italic text-emerald-400">hood</span></h2>
				<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-10 font-mono text-lg leading-loose text-white/60">
					<pre class="text-white/60">
SvelteKit + TypeScript + TailwindCSS
        |
      NGINX (reverse proxy)
        |
FastAPI (Python 3.12, fully async)
        |
   +---------+---------+---------+
   |         |         |         |
PostgreSQL  Redis   M-Pesa    Claude AI
 (asyncpg)  (cache)  (Daraja)  (OpenRouter)
                       |
                    eSMS Mail
                   (transactional)
					</pre>
				</div>
				<div class="fragment fade-in mt-6 flex flex-wrap gap-3">
					{#each ['14 API routers', '10 DB models', '24 routes', '5 integrations', 'Docker + CI/CD'] as tag}
						<span class="rounded-full border border-white/[0.08] bg-white/[0.02] px-4 py-2 text-sm text-white/50">{tag}</span>
					{/each}
				</div>
			</div>
		</section>

		<!-- ==================== DEMO ==================== -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="flex flex-col items-center justify-center">
				<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 mb-6 font-medium">Live Demo</p>
				<h2 class="font-serif text-8xl text-white mb-8">
					Let us <span class="italic text-emerald-400">show you.</span>
				</h2>
				<div class="flex items-center gap-3 rounded-2xl border border-emerald-500/20 bg-emerald-500/[0.05] px-8 py-4">
					<span class="relative flex h-3 w-3"><span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-emerald-400 opacity-75"></span><span class="relative inline-flex h-3 w-3 rounded-full bg-emerald-400"></span></span>
					<p class="text-2xl text-emerald-400 font-mono">flowai.cash</p>
				</div>
			</div>
		</section>

		<!-- ==================== TEAM ==================== -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 mb-6 font-medium">The Team</p>
				<h2 class="font-serif text-5xl text-white mb-12">
					<span class="italic text-emerald-400">Gatekeepers</span> Group
				</h2>
				<div class="grid grid-cols-5 gap-6">
					{#each [
						{ name: 'Steve Tom', role: 'Lead Dev & Frontend', img: '/team/steve.jpg' },
						{ name: 'Oliver Jackson', role: 'Security & Infra', img: '/team/oliver.jpg' },
						{ name: 'Beth Kimani', role: 'AI & Product', img: '/team/beth.jpg' },
						{ name: 'Stanley Onyango', role: 'Backend & Payments', img: '/team/stanley.jpg' },
						{ name: 'Osborne Nyakaru', role: 'AI & Data', img: '/team/osbon.jpg' },
					] as member}
						<div class="text-center">
							<img src={member.img} alt={member.name} class="w-36 h-36 mx-auto rounded-2xl object-cover border-2 border-white/[0.06] mb-4" />
							<p class="text-lg text-white font-medium">{member.name}</p>
							<p class="text-sm text-emerald-400/70 mt-1">{member.role}</p>
						</div>
					{/each}
				</div>
			</div>
		</section>

		<!-- ==================== THE ASK ==================== -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 mb-6 font-medium">The Ask</p>
				<h2 class="font-serif text-5xl text-white mb-12">What we <span class="italic text-emerald-400">need</span></h2>
				<div class="grid grid-cols-3 gap-6">
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8" data-fragment-index="0">
						<p class="font-serif text-4xl text-white italic mb-4">50</p>
						<p class="text-xl text-white/60 font-medium mb-2">Pilot Businesses</p>
						<p class="text-base text-white/30">3-month beta to validate retention and transaction volume</p>
					</div>
					<div class="fragment fade-up rounded-2xl border border-white/[0.06] bg-white/[0.02] p-8" data-fragment-index="1">
						<p class="font-serif text-4xl text-emerald-400 italic mb-4">Safaricom</p>
						<p class="text-xl text-white/60 font-medium mb-2">Ecosystem Access</p>
						<p class="text-base text-white/30">Daraja partnerships team and SME network introductions</p>
					</div>
					<div class="fragment fade-up rounded-2xl border border-emerald-500/20 bg-emerald-500/[0.03] p-8" data-fragment-index="2">
						<p class="font-serif text-4xl text-emerald-400 italic mb-4">KES 2M</p>
						<p class="text-xl text-white/60 font-medium mb-2">Seed Funding</p>
						<p class="text-base text-white/30">12-month runway &rarr; 500 businesses, KES 200K+ MRR</p>
					</div>
				</div>
			</div>
		</section>

		<!-- ==================== TRY IT ==================== -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="text-left max-w-5xl mx-auto">
				<p class="text-sm uppercase tracking-[0.3em] text-emerald-500 mb-6 font-medium">Try It Now</p>
				<h2 class="font-serif text-5xl text-white mb-12">Scan. Open. <span class="italic text-emerald-400">Explore.</span></h2>
				<div class="grid grid-cols-2 gap-12">
					<div class="text-center">
						{#if qrApp}
							<img src={qrApp} alt="QR App" class="mx-auto h-52 w-52 mb-6" />
						{/if}
						<p class="text-2xl text-emerald-400 font-medium mb-2">flowai.cash</p>
						<p class="text-base text-white/40">Open the app &middot; Create an account &middot; Try it live</p>
					</div>
					<div class="text-center">
						{#if qrDemo}
							<img src={qrDemo} alt="QR Demo" class="mx-auto h-52 w-52 mb-6" />
						{/if}
						<p class="text-2xl text-white font-medium mb-2">flowai.cash/demo</p>
						<p class="text-base text-white/40">Follow along &middot; QR codes &middot; Instructions</p>
					</div>
				</div>
			</div>
		</section>

		<!-- ==================== CLOSING ==================== -->
		<section data-auto-animate data-background-color="#09090b">
			<div class="flex flex-col items-center justify-center text-center max-w-4xl mx-auto">
				<img src="/logo-gold.png" alt="CashFlow AI" class="w-20 h-20 mb-8" data-id="logo" />
				<h2 class="font-serif text-6xl text-white leading-tight mb-8" data-id="closing">
					We're not pitching an idea.<br/>
					<span class="italic text-emerald-400">We're demonstrating a solution.</span>
				</h2>
				<p class="text-2xl text-white/30 mb-12">flowai.cash</p>
				<p class="text-lg text-white/20">CashFlow AI &middot; Built by Gatekeepers Group &middot; Nairobi, 2026</p>
			</div>
		</section>

	</div>
</div>

<style>
	:global(html), :global(body) {
		margin: 0;
		padding: 0;
		height: 100%;
		overflow: hidden;
		background: #09090b;
	}
	:global(.reveal) {
		font-family: 'DM Sans', sans-serif;
		height: 100vh;
	}
	:global(.reveal .slide-background) {
		background: #09090b;
	}
	:global(.reveal h1),
	:global(.reveal h2),
	:global(.reveal h3) {
		font-family: 'Instrument Serif', serif;
		text-transform: none;
		font-weight: 400;
		color: white;
	}
	:global(.reveal) {
		color: rgba(255,255,255,0.7);
	}
	:global(.reveal .slides section) {
		padding: 40px 60px;
		text-align: left;
	}
	:global(.reveal .controls) {
		color: #10b981;
	}
	:global(.reveal .progress span) {
		background: #10b981;
	}
	/* Tailwind-like utilities for reveal */
	.font-serif { font-family: 'Instrument Serif', serif; }
	.font-mono { font-family: 'JetBrains Mono', 'SF Mono', monospace; }
	.animate-ping { animation: ping 1s cubic-bezier(0, 0, 0.2, 1) infinite; }
	.animate-pulse { animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite; }
	@keyframes ping { 75%, 100% { transform: scale(2); opacity: 0; } }
	@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: .5; } }
</style>
