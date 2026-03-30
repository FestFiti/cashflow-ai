<script lang="ts">

	interface Props {
		isDark: boolean;
		featuresVisible: boolean;
	}

	let { isDark, featuresVisible }: Props = $props();
</script>

<!-- FEATURES -->
<section id="features" class="relative py-28 transition-colors {isDark ? 'bg-zinc-950' : 'bg-white'}">
	<div class="mx-auto max-w-7xl px-6">
		<div
			class="mb-16 transition-all duration-700 {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}"
		>
			<p class="mb-3 text-[12px] font-semibold uppercase tracking-[0.2em] text-emerald-500" style="font-family: 'DM Sans', sans-serif;">Features</p>
			<h2 class="max-w-lg font-['Instrument_Serif'] text-4xl leading-tight tracking-tight md:text-5xl {isDark ? 'text-white' : 'text-zinc-900'}">
				Everything you need to <span class="italic text-emerald-400">manage your cash flow</span>
			</h2>
		</div>

		<div class="grid grid-cols-1 gap-4 md:grid-cols-6" style="font-family: 'DM Sans', sans-serif;">
			<!-- AI Invoice Generation — wide, sparkle particles -->
			<div
				class="group relative overflow-hidden rounded-2xl border p-8 md:col-span-4 transition-all duration-500 hover:border-violet-500/20 {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'} {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
				style="transition-delay: 200ms;"
			>
				<!-- Floating sparkle particles -->
				<div class="pointer-events-none absolute inset-0 overflow-hidden">
					{#each [
						{ x: 80, y: 15, s: 6, d: 4.0 }, { x: 70, y: 40, s: 4, d: 3.2 }, { x: 90, y: 60, s: 5, d: 3.8 },
						{ x: 60, y: 25, s: 3, d: 4.5 }, { x: 85, y: 80, s: 4, d: 3.5 }, { x: 75, y: 55, s: 3, d: 4.2 },
					] as p}
						<div class="absolute rounded-full {isDark ? 'bg-violet-400' : 'bg-violet-500'}" style="left:{p.x}%;top:{p.y}%;width:{p.s}px;height:{p.s}px;animation:mail-float {p.d}s ease-in-out infinite;animation-delay:{p.d*0.2}s;"></div>
					{/each}
				</div>
				<div class="absolute -right-12 -top-12 h-44 w-44 rounded-full opacity-[0.05]" style="background:radial-gradient(circle,#8b5cf6 0%,transparent 70%);"></div>
				<div class="relative">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-violet-500/20 bg-violet-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z" />
						</svg>
					</div>
					<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">AI Invoice Generation</h3>
					<p class="mb-5 max-w-sm text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">Describe a transaction in plain language. AI parses it into a professional invoice with payment details.</p>
					<!-- Faux typing line -->
					<div class="flex items-center gap-2 rounded-lg border px-3 py-2 {isDark ? 'border-white/[0.06] bg-white/[0.02]' : 'border-zinc-200 bg-white'}">
						<span class="text-[12px] {isDark ? 'text-white/25' : 'text-zinc-400'}">Generate invoice for web design, 50k...</span>
						<div class="h-4 w-[2px] rounded-full bg-violet-400" style="animation: cursor-blink 1s step-end infinite;"></div>
					</div>
				</div>
			</div>

			<!-- M-Pesa Payments — tall card, phone mockup lines -->
			<div
				class="group relative overflow-hidden rounded-2xl border p-8 md:col-span-2 md:row-span-2 transition-all duration-500 hover:border-emerald-500/20 {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'} {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
				style="transition-delay: 280ms;"
			>
				<!-- Animated concentric rings (signal from phone) -->
				<div class="pointer-events-none absolute inset-0 overflow-hidden">
					{#each Array(3) as _, r}
						<div
							class="absolute rounded-full border {isDark ? 'border-emerald-500/[0.06]' : 'border-emerald-400/10'}"
							style="width:{100 + r*60}px;height:{100 + r*60}px;top:50%;left:50%;transform:translate(-50%,-50%);animation:ring-expand 3s ease-out infinite;animation-delay:{r*1}s;"
						></div>
					{/each}
				</div>
				<div class="relative flex h-full flex-col">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-emerald-500/20 bg-emerald-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3" />
						</svg>
					</div>
					<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">M-Pesa Payments</h3>
					<p class="mb-auto text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">STK Push payment links, B2C disbursements, and real-time payment confirmations via Daraja API.</p>
					<!-- Fake notification -->
					<div class="mt-6 rounded-lg border px-3 py-2.5 {isDark ? 'border-emerald-500/15 bg-emerald-500/[0.04]' : 'border-emerald-200 bg-emerald-50'}">
						<div class="flex items-center gap-2">
							<div class="h-1.5 w-1.5 rounded-full bg-emerald-400" style="animation:pulse-dot 2s ease-in-out infinite;"></div>
							<span class="text-[11px] font-medium text-emerald-400">KES 15,000 received</span>
						</div>
						<p class="mt-1 text-[10px] {isDark ? 'text-emerald-400/40' : 'text-emerald-600/50'}">M-Pesa • QK7A2...3F • just now</p>
					</div>
				</div>
			</div>

			<!-- Smart Reminders — with animated bell pulse -->
			<div
				class="group relative overflow-hidden rounded-2xl border p-8 md:col-span-2 transition-all duration-500 hover:border-amber-500/20 {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'} {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
				style="transition-delay: 360ms;"
			>
				<!-- Ripple rings from icon -->
				<div class="pointer-events-none absolute left-8 top-8 overflow-visible">
					{#each Array(2) as _, r}
						<div
							class="absolute rounded-full border {isDark ? 'border-amber-500/[0.08]' : 'border-amber-400/15'}"
							style="width:{50 + r*30}px;height:{50 + r*30}px;top:{-(r*15)}px;left:{-(r*15)}px;animation:ring-expand 4s ease-out infinite;animation-delay:{r*1.5}s;"
						></div>
					{/each}
				</div>
				<div class="relative">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-amber-500/20 bg-amber-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5" style="animation:bell-ring 3s ease-in-out infinite;">
							<path stroke-linecap="round" stroke-linejoin="round" d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
						</svg>
					</div>
					<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">Smart Reminders</h3>
					<p class="text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">AI drafts personalised reminders and schedules them at optimal intervals via Ratiba.</p>
				</div>
			</div>

			<!-- Real-Time Dashboard — with horizontal sliding bars -->
			<div
				class="group relative overflow-hidden rounded-2xl border p-8 md:col-span-2 transition-all duration-500 hover:border-blue-500/20 {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'} {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
				style="transition-delay: 440ms;"
			>
				<div class="relative">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-blue-500/20 bg-blue-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5m.75-9l3-3 2.148 2.148A12.061 12.061 0 0116.5 7.605" />
						</svg>
					</div>
					<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">Real-Time Dashboard</h3>
					<p class="mb-5 text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">WebSocket-powered live updates. See payments land, overdue alerts pulse, and AI commentary roll in.</p>
					<!-- Mini animated bars -->
					<div class="flex items-end gap-[3px]">
						{#each Array(20) as _, b}
							<div
								class="w-1.5 rounded-t transition-all {b < 14 ? 'bg-blue-500/40' : 'bg-blue-500/20'}"
								style="height:{6 + Math.abs(Math.sin(b * 0.7)) * 18}px;animation:bar-breathe {2 + (b % 4) * 0.3}s ease-in-out infinite;animation-delay:{b * 0.08}s;"
							></div>
						{/each}
					</div>
				</div>
			</div>

			<!-- Team Management — outer dot grid + avatar circles -->
			<div
				class="group relative md:col-span-3 transition-all duration-500 {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
				style="transition-delay: 520ms;"
			>
				<!-- Outer dot grid -->
				<div class="team-dots pointer-events-none absolute -inset-4 {isDark ? 'opacity-[0.03]' : 'opacity-[0.06]'}" style="background-image:radial-gradient(circle,{isDark ? '#10b981' : '#059669'} 1px,transparent 1px);background-size:14px 14px;"></div>
				<div class="relative overflow-hidden rounded-2xl border p-8 {isDark ? 'border-white/[0.04] bg-zinc-950/80' : 'border-zinc-200 bg-white'} backdrop-blur-sm hover:border-emerald-500/20 transition-all">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-emerald-500/20 bg-emerald-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z" />
						</svg>
					</div>
					<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">Team Management</h3>
					<p class="mb-5 text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">Invite your accountant, manager, or sales team. Role-based permissions keep everyone in their lane.</p>
					<!-- Role badges -->
					<div class="flex flex-wrap gap-2">
						{#each ['Admin', 'Manager', 'Accountant', 'Sales'] as role, r}
							<span class="rounded-full border px-3 py-1 text-[11px] font-medium {isDark ? 'border-white/[0.06] bg-white/[0.02] text-white/40' : 'border-zinc-200 bg-white text-zinc-500'}" style="animation:mail-float {3 + r * 0.5}s ease-in-out infinite;animation-delay:{r * 0.4}s;">{role}</span>
						{/each}
					</div>
				</div>
			</div>

			<!-- Cash Flow Forecasting — ascending chart animation -->
			<div
				class="group relative overflow-hidden rounded-2xl border p-8 md:col-span-3 transition-all duration-500 hover:border-emerald-500/20 {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'} {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
				style="transition-delay: 600ms;"
			>
				<!-- Subtle rising gradient -->
				<div class="pointer-events-none absolute bottom-0 left-0 right-0 h-1/2 opacity-[0.04]" style="background:linear-gradient(to top, #10b981, transparent);"></div>
				<div class="relative">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-emerald-500/20 bg-emerald-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941" />
						</svg>
					</div>
					<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">Cash Flow Forecasting</h3>
					<p class="mb-5 text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">AI predicts upcoming payment gaps and recommends actions before problems arise.</p>
					<!-- Animated ascending bars chart -->
					<div class="flex items-end gap-1">
						{#each [20, 28, 22, 35, 30, 42, 38, 50, 45, 58, 52, 65] as h, c}
							<div
								class="flex-1 rounded-t {c >= 10 ? 'bg-emerald-400/60' : c >= 7 ? 'bg-emerald-500/40' : 'bg-emerald-500/25'}"
								style="height:{h}px;animation:bar-grow 1.5s ease-out forwards;animation-delay:{c * 0.1}s;"
							></div>
						{/each}
					</div>
				</div>
			</div>
		</div>
	</div>
</section>
