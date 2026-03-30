<script lang="ts">
	interface Props {
		isDark: boolean;
		featuresVisible: boolean;
	}

	let { isDark, featuresVisible }: Props = $props();

	// Deterministic bar heights to avoid SSR/hydration mismatch
	const forecastBars = [20, 28, 22, 35, 30, 42, 38, 50, 45, 58, 52, 65];
	const dashBars     = [8, 14, 10, 22, 18, 24, 12, 20, 16, 26, 14, 22, 18, 20, 12, 24, 10, 20, 16, 18];
	const waveBars     = [10, 16, 20, 18, 24, 14, 22, 12, 20, 18, 24, 14, 22, 16, 18, 12];
</script>

<!-- ─────────────────────────────────────────────── FEATURES ── -->
<section
		id="features"
		class="relative py-28 transition-colors {isDark ? 'bg-zinc-950' : 'bg-white'}"
>
	<div class="mx-auto max-w-7xl px-6">

		<!-- Section header -->
		<div
				class="mb-16 transition-all duration-700
                {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-6 opacity-0'}"
		>
			<p
					class="mb-3 text-[12px] font-semibold uppercase tracking-[0.2em] text-emerald-500"
					style="font-family:'DM Sans',sans-serif;"
			>Features</p>
			<h2
					class="max-w-lg font-['Instrument_Serif'] text-4xl leading-tight tracking-tight md:text-5xl
                   {isDark ? 'text-white' : 'text-zinc-900'}"
			>
				Everything you need to
				<span class="italic text-emerald-400">manage your cash flow</span>
			</h2>
		</div>

		<!-- Bento grid -->
		<div class="grid grid-cols-1 gap-6 md:grid-cols-6" style="font-family:'DM Sans',sans-serif;">

			<!-- ══════════════════════════════════════════════════════
                 CARD 1 · AI Invoice Generation  (col-span-4)
                 violet · bleeding lines · dot grid · generation shimmer
            ════════════════════════════════════════════════════════ -->
			<div
					class="group relative md:col-span-4 transition-all duration-500
                   {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
					style="transition-delay:200ms;"
			>
				<!-- Bleeding dot grid -->
				<div
						class="ai-dots pointer-events-none absolute -inset-6
                      {isDark ? 'opacity-[0.045]' : 'opacity-[0.08]'}"
						style="background-image:radial-gradient(circle,{isDark ? '#8b5cf6' : '#7c3aed'} 1.5px,transparent 1.5px);
                      background-size:16px 16px;"
				></div>

				<!-- Bleeding cross-lines (violet) -->
				<div class="pointer-events-none absolute -inset-4 opacity-25 transition-opacity group-hover:opacity-50">
					<div class="absolute top-[10px] -left-[15px] h-[1px] w-[calc(100%+30px)]
                           {isDark ? 'bg-violet-500/60' : 'bg-violet-500/50'}"></div>
					<div class="absolute bottom-[10px] -right-[15px] h-[1px] w-[calc(100%+30px)]
                           {isDark ? 'bg-violet-500/60' : 'bg-violet-500/50'}"></div>
					<div class="absolute -top-[15px] left-[10px] h-[calc(100%+30px)] w-[1px]
                           {isDark ? 'bg-violet-500/60' : 'bg-violet-500/50'}"></div>
					<div class="absolute -bottom-[15px] right-[10px] h-[calc(100%+30px)] w-[1px]
                           {isDark ? 'bg-violet-500/60' : 'bg-violet-500/50'}"></div>
				</div>

				<!-- Card surface -->
				<div
						class="relative overflow-hidden rounded-2xl border p-8 h-full
                      transition-all duration-500 hover:border-violet-500/25
                      {isDark ? 'border-white/[0.04] bg-zinc-950/80' : 'border-zinc-200 bg-zinc-50'}
                      backdrop-blur-sm"
				>
					<!-- Radial glow (morphing border-radius) -->
					<div
							class="pointer-events-none absolute -right-14 -top-14 h-52 w-52 opacity-[0.07]"
							style="background:radial-gradient(circle,#8b5cf6 0%,transparent 70%);
                         animation:radius-morph 8s ease-in-out infinite;"
					></div>

					<!-- Floating sparkle particles -->
					<div class="pointer-events-none absolute inset-0 overflow-hidden">
						{#each [
							{ x:82, y:12, s:5, d:4.0 }, { x:71, y:38, s:3, d:3.2 }, { x:91, y:58, s:4, d:3.8 },
							{ x:62, y:22, s:3, d:4.5 }, { x:87, y:75, s:4, d:3.5 }, { x:76, y:50, s:3, d:4.2 },
							{ x:55, y:65, s:2, d:5.0 }, { x:95, y:30, s:3, d:3.6 },
						] as p}
							<div
									class="absolute rounded-full {isDark ? 'bg-violet-400' : 'bg-violet-500'}"
									style="left:{p.x}%;top:{p.y}%;width:{p.s}px;height:{p.s}px;
                               opacity:.5;animation:mail-float {p.d}s ease-in-out infinite;
                               animation-delay:{p.d * 0.3}s;"
							></div>
						{/each}
					</div>

					<div class="relative">
						<!-- Icon -->
						<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl
                              border border-violet-500/20 bg-violet-500/[0.08]">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-violet-400"
							     fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round"
								      d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.455 2.456L21.75 6l-1.036.259a3.375 3.375 0 00-2.455 2.456z"/>
							</svg>
						</div>

						<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">
							AI Invoice Generation
						</h3>
						<p class="mb-6 max-w-sm text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">
							Describe a transaction in plain language. AI parses it into a professional invoice with payment details.
						</p>

						<!-- ── Generation UI mockup ── -->
						<div class="rounded-xl border overflow-hidden
                              {isDark ? 'border-white/[0.06] bg-black/30' : 'border-zinc-200 bg-white'}">

							<!-- Prompt input row -->
							<div class="flex items-center gap-2 border-b px-4 py-3
                                 {isDark ? 'border-white/[0.05]' : 'border-zinc-100'}">
								<div class="flex h-5 w-5 items-center justify-center rounded-md bg-violet-500/20">
									<div class="h-2 w-2 rounded-full bg-violet-400"></div>
								</div>
								<span class="text-[12px] {isDark ? 'text-white/30' : 'text-zinc-400'}">
                           Generate invoice for web design, 50k KES…
                        </span>
								<div
										class="h-3.5 w-[1.5px] rounded-full bg-violet-400 ml-0.5"
										style="animation:cursor-blink 1s step-end infinite;"
								></div>
							</div>

							<!-- Generated content lines with shimmer -->
							<div class="relative px-4 py-4 space-y-2.5 overflow-hidden">
								<!-- Shimmer scan -->
								<div
										class="pointer-events-none absolute inset-0"
										style="animation:gen-scan 3s ease-in-out infinite;animation-delay:0.5s;"
								>
									<div class="absolute inset-y-0 w-24"
									     style="background:linear-gradient(to right,transparent,{isDark ? 'rgba(139,92,246,0.12)' : 'rgba(139,92,246,0.07)'},transparent);">
									</div>
								</div>

								<!-- Line 1 — label + value -->
								{#each [
									{ label:'Client',   val:'Acme Corp Ltd',   w:'w-24', vw:'w-32', d:'0s'   },
									{ label:'Service',  val:'Web Design',       w:'w-20', vw:'w-28', d:'0.15s' },
									{ label:'Amount',   val:'KES 50,000',       w:'w-16', vw:'w-24', d:'0.30s' },
									{ label:'Due Date', val:'Apr 14, 2026',     w:'w-20', vw:'w-28', d:'0.45s' },
								] as row}
									<div class="flex items-center gap-3"
									     style="animation:gen-line-in 0.5s ease-out both;animation-delay:{row.d};">
										<div class="h-2 {row.w} rounded-full
                                          {isDark ? 'bg-white/10' : 'bg-zinc-200'}"></div>
										<div class="h-2 {row.vw} rounded-full
                                          {isDark ? 'bg-violet-400/30' : 'bg-violet-400/40'}"></div>
									</div>
								{/each}

								<!-- Bottom status chip -->
								<div class="mt-3 flex items-center gap-2">
									<div class="h-1.5 w-1.5 rounded-full bg-violet-400"
									     style="animation:pulse-dot 1.6s ease-in-out infinite;"></div>
									<span class="text-[11px] font-medium text-violet-400">Generating…</span>
								</div>
							</div>
						</div>
					</div>

					<!-- Bottom wave -->
					<div class="pointer-events-none absolute bottom-0 left-0 right-0 h-12 overflow-hidden
                           {isDark ? 'opacity-[0.04]' : 'opacity-[0.05]'}">
						<svg class="wave-svg absolute bottom-0 text-violet-400"
						     style="width:200%;animation:wave-flow 10s linear infinite;"
						     viewBox="0 0 1440 48" preserveAspectRatio="none" fill="currentColor">
							<path d="M0,24 C120,40 240,8 360,24 C480,40 600,8 720,24
                              C840,40 960,8 1080,24 C1200,40 1320,8 1440,24
                              C1560,40 1680,8 1800,24 C1920,40 2040,8 2160,24
                              C2280,40 2400,8 2520,24 C2640,40 2760,8 2880,24 L2880,48 L0,48 Z"/>
						</svg>
					</div>
				</div>
			</div>

			<!-- ══════════════════════════════════════════════════════
                 CARD 2 · M-Pesa Payments  (col-span-2, row-span-2)
                 emerald · concentric rings · wave bottom
            ════════════════════════════════════════════════════════ -->
			<div
					class="group relative overflow-hidden rounded-2xl border p-8 md:col-span-2 md:row-span-2
                   transition-all duration-500 hover:border-emerald-500/25
                   {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'}
                   {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
					style="transition-delay:280ms;"
			>
				<!-- Concentric ring animations -->
				<div class="pointer-events-none absolute inset-0 overflow-hidden">
					{#each [0,1,2] as r}
						<div
								class="absolute rounded-full border
                            {isDark ? 'border-emerald-500/[0.07]' : 'border-emerald-400/12'}"
								style="width:{90+r*64}px;height:{90+r*64}px;top:50%;left:50%;
                            transform:translate(-50%,-50%);
                            animation:ring-expand 3.5s ease-out infinite;
                            animation-delay:{r * 1.1}s;"
						></div>
					{/each}
				</div>

				<!-- Morphing glow blob -->
				<div
						class="pointer-events-none absolute -bottom-10 -right-10 h-40 w-40 opacity-[0.06]"
						style="background:radial-gradient(circle,#10b981 0%,transparent 70%);
                      animation:radius-morph 9s ease-in-out infinite reverse;"
				></div>

				<div class="relative flex h-full flex-col">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl
                           border border-emerald-500/20 bg-emerald-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400"
						     fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round"
							      d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3"/>
						</svg>
					</div>

					<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">
						M-Pesa Payments
					</h3>
					<p class="mb-auto text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">
						STK Push payment links, B2C disbursements, and real-time payment confirmations via Daraja API.
					</p>

					<!-- Transaction feed -->
					<div class="mt-6 space-y-2">
						{#each [
							{ amount:'KES 15,000', ref:'QK7A2...3F', delay:'0s',   age:'just now' },
							{ amount:'KES 8,500',  ref:'PR3B9...1D', delay:'0.6s',  age:'2 min ago' },
							{ amount:'KES 32,000', ref:'MN5C4...7K', delay:'1.2s', age:'5 min ago' },
						] as tx, i}
							<div
									class="rounded-lg border px-3 py-2.5 transition-all
                               {isDark ? 'border-emerald-500/12 bg-emerald-500/[0.03]'
                                       : 'border-emerald-200 bg-emerald-50'}"
									style="animation:gen-line-in 0.5s ease-out both;animation-delay:{tx.delay};"
							>
								<div class="flex items-center justify-between">
									<div class="flex items-center gap-2">
										<div
												class="h-1.5 w-1.5 rounded-full bg-emerald-400"
												style="animation:pulse-dot 2s ease-in-out infinite;animation-delay:{i*0.4}s;"
										></div>
										<span class="text-[11px] font-medium text-emerald-400">{tx.amount}</span>
									</div>
									<span class="text-[10px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{tx.age}</span>
								</div>
								<p class="mt-0.5 text-[10px] {isDark ? 'text-emerald-400/35' : 'text-emerald-600/50'}">
									M-Pesa · {tx.ref}
								</p>
							</div>
						{/each}
					</div>
				</div>

				<!-- Bottom wave -->
				<div class="pointer-events-none absolute bottom-0 left-0 right-0 h-10 overflow-hidden
                        {isDark ? 'opacity-[0.04]' : 'opacity-[0.05]'}">
					<svg class="absolute bottom-0 text-emerald-400"
					     style="width:200%;animation:wave-flow 12s linear infinite reverse;"
					     viewBox="0 0 1440 40" preserveAspectRatio="none" fill="currentColor">
						<path d="M0,20 C120,34 240,6 360,20 C480,34 600,6 720,20
                           C840,34 960,6 1080,20 C1200,34 1320,6 1440,20
                           C1560,34 1680,6 1800,20 C1920,34 2040,6 2160,20
                           C2280,34 2400,6 2520,20 C2640,34 2760,6 2880,20 L2880,40 L0,40 Z"/>
					</svg>
				</div>
			</div>

			<!-- ══════════════════════════════════════════════════════
                 CARD 3 · Smart Reminders  (col-span-2)
                 amber · bell animation · notification stack · ripple rings
            ════════════════════════════════════════════════════════ -->
			<div
					class="group relative overflow-hidden rounded-2xl border p-8 md:col-span-2
                   transition-all duration-500 hover:border-amber-500/25
                   {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'}
                   {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
					style="transition-delay:360ms;"
			>
				<!-- Ripple rings from icon corner -->
				<div class="pointer-events-none absolute left-8 top-8 overflow-visible">
					{#each [0,1] as r}
						<div
								class="absolute rounded-full border
                            {isDark ? 'border-amber-500/[0.09]' : 'border-amber-400/15'}"
								style="width:{48+r*36}px;height:{48+r*36}px;
                            top:{-(r*18)}px;left:{-(r*18)}px;
                            animation:ring-expand 4s ease-out infinite;
                            animation-delay:{r*1.6}s;"
						></div>
					{/each}
				</div>

				<div class="relative">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl
                           border border-amber-500/20 bg-amber-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-amber-400"
						     fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5"
						     style="animation:bell-ring 3s ease-in-out infinite;">
							<path stroke-linecap="round" stroke-linejoin="round"
							      d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0"/>
						</svg>
					</div>

					<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">
						Smart Reminders
					</h3>
					<p class="mb-5 text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">
						AI drafts personalised reminders and schedules them at optimal intervals via Ratiba.
					</p>

					<!-- Stacked notification cards -->
					<div class="space-y-2">
						{#each [
							{ msg:'Invoice #047 due in 2 days', d:'0s', iconPath:'M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m0 12.75h7.5m-7.5 3H12M10.5 2.25H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z' },
							{ msg:'Reminder sent to Acme Corp', d:'0.3s', iconPath:'M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75' },
						] as n}
							<div
									class="flex items-center gap-2.5 rounded-lg border px-3 py-2.5
                               {isDark ? 'border-amber-500/12 bg-amber-500/[0.03]'
                                       : 'border-amber-200 bg-amber-50'}"
									style="animation:mail-float {3.5}s ease-in-out infinite;animation-delay:{n.d};"
							>
								<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 flex-shrink-0 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
									<path stroke-linecap="round" stroke-linejoin="round" d={n.iconPath} />
								</svg>
								<span class="text-[11px] leading-relaxed {isDark ? 'text-amber-400/70' : 'text-amber-700/80'}">
                           {n.msg}
                        </span>
							</div>
						{/each}
					</div>
				</div>
			</div>

			<!-- ══════════════════════════════════════════════════════
                 CARD 4 · Real-Time Dashboard  (col-span-2)
                 blue · bleeding lines · animated wave bars · live dot
            ════════════════════════════════════════════════════════ -->
			<div
					class="group relative md:col-span-2 transition-all duration-500
                   {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
					style="transition-delay:440ms;"
			>
				<!-- Bleeding cross-lines (blue) -->
				<div class="pointer-events-none absolute -inset-4 opacity-20 transition-opacity group-hover:opacity-45">
					<div class="absolute top-[10px] left-[10px] h-[1px] w-[calc(100%-20px)]
                           {isDark ? 'bg-blue-500/60' : 'bg-blue-500/50'}"></div>
					<div class="absolute bottom-[10px] right-[10px] h-[1px] w-[calc(100%-20px)]
                           {isDark ? 'bg-blue-500/60' : 'bg-blue-500/50'}"></div>
					<div class="absolute top-[10px] left-[10px] h-[calc(100%-20px)] w-[1px]
                           {isDark ? 'bg-blue-500/60' : 'bg-blue-500/50'}"></div>
					<div class="absolute bottom-[10px] right-[10px] h-[calc(100%-20px)] w-[1px]
                           {isDark ? 'bg-blue-500/60' : 'bg-blue-500/50'}"></div>
				</div>

				<!-- Card surface -->
				<div
						class="relative overflow-hidden rounded-2xl border p-8 h-full
                      transition-all duration-500 hover:border-blue-500/25
                      {isDark ? 'border-white/[0.04] bg-zinc-950/80' : 'border-zinc-200 bg-zinc-50'}
                      backdrop-blur-sm"
				>
					<!-- Morphing glow -->
					<div
							class="pointer-events-none absolute -left-10 -bottom-10 h-40 w-40 opacity-[0.05]"
							style="background:radial-gradient(circle,#3b82f6 0%,transparent 70%);
                         animation:radius-morph 11s ease-in-out infinite;"
					></div>

					<div class="relative">
						<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl
                              border border-blue-500/20 bg-blue-500/[0.08]">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-400"
							     fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round"
								      d="M3.75 3v11.25A2.25 2.25 0 006 16.5h2.25M3.75 3h-1.5m1.5 0h16.5m0 0h1.5m-1.5 0v11.25A2.25 2.25 0 0118 16.5h-2.25m-7.5 0h7.5m-7.5 0l-1 3m8.5-3l1 3m0 0l.5 1.5m-.5-1.5h-9.5m0 0l-.5 1.5m.75-9l3-3 2.148 2.148A12.061 12.061 0 0116.5 7.605"/>
							</svg>
						</div>

						<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">
							Real-Time Dashboard
						</h3>

						<!-- Live indicator -->
						<div class="mb-4 flex items-center gap-2">
							<div class="h-1.5 w-1.5 rounded-full bg-blue-400"
							     style="animation:pulse-dot 1.4s ease-in-out infinite;"></div>
							<span class="text-[11px] font-medium text-blue-400">Live</span>
						</div>

						<p class="mb-5 text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">
							WebSocket-powered live updates. See payments land, overdue alerts pulse, and AI commentary roll in.
						</p>

						<!-- Animated wave bars -->
						<div class="flex items-end gap-[3px]">
							{#each dashBars as h, b}
								<div
										class="w-1.5 rounded-t transition-all
                                  {b < 14 ? 'bg-blue-500/50' : 'bg-blue-500/20'}"
										style="height:{h}px;
                                  animation:bar-breathe {2+(b%4)*0.3}s ease-in-out infinite;
                                  animation-delay:{b*0.08}s;"
								></div>
							{/each}
						</div>
					</div>
				</div>
			</div>

			<!-- ══════════════════════════════════════════════════════
                 CARD 5 · Team Management  (col-span-3)
                 emerald · bleeding dot grid · role badges
            ════════════════════════════════════════════════════════ -->
			<div
					class="group relative md:col-span-3 transition-all duration-500
                   {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
					style="transition-delay:520ms;"
			>
				<!-- Bleeding cross-lines (blue) -->
				<div class="pointer-events-none absolute -inset-4 opacity-20 transition-opacity group-hover:opacity-45">
					<div class="absolute top-[10px] -left-[15px] h-[1px] w-[calc(100%+30px)]
                           {isDark ? 'bg-blue-500/60' : 'bg-blue-500/50'}"></div>
					<div class="absolute bottom-[10px] -right-[15px] h-[1px] w-[calc(100%+30px)]
                           {isDark ? 'bg-blue-500/60' : 'bg-blue-500/50'}"></div>
					<div class="absolute -top-[15px] left-[10px] h-[calc(100%+30px)] w-[1px]
                           {isDark ? 'bg-blue-500/60' : 'bg-blue-500/50'}"></div>
					<div class="absolute -bottom-[15px] right-[10px] h-[calc(100%+30px)] w-[1px]
                           {isDark ? 'bg-blue-500/60' : 'bg-blue-500/50'}"></div>
				</div>

				<!-- Bleeding dot grid -->
				<div
						class="team-dots pointer-events-none absolute -inset-5
                      {isDark ? 'opacity-[0.035]' : 'opacity-[0.06]'}"
						style="background-image:radial-gradient(circle,{isDark ? '#10b981' : '#059669'} 1px,transparent 1px);
                      background-size:14px 14px;"
				></div>

				<div
						class="relative overflow-hidden rounded-2xl border p-8 h-full
                      transition-all duration-500 hover:border-emerald-500/25
                      {isDark ? 'border-white/[0.04] bg-zinc-950/80' : 'border-zinc-200 bg-white'}
                      backdrop-blur-sm"
				>
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl
                           border border-emerald-500/20 bg-emerald-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400"
						     fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round"
							      d="M18 18.72a9.094 9.094 0 003.741-.479 3 3 0 00-4.682-2.72m.94 3.198l.001.031c0 .225-.012.447-.037.666A11.944 11.944 0 0112 21c-2.17 0-4.207-.576-5.963-1.584A6.062 6.062 0 016 18.719m12 0a5.971 5.971 0 00-.941-3.197m0 0A5.995 5.995 0 0012 12.75a5.995 5.995 0 00-5.058 2.772m0 0a3 3 0 00-4.681 2.72 8.986 8.986 0 003.74.477m.94-3.197a5.971 5.971 0 00-.94 3.197M15 6.75a3 3 0 11-6 0 3 3 0 016 0zm6 3a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0zm-13.5 0a2.25 2.25 0 11-4.5 0 2.25 2.25 0 014.5 0z"/>
						</svg>
					</div>

					<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">
						Team Management
					</h3>
					<p class="mb-5 text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">
						Invite your accountant, manager, or sales team. Role-based permissions keep everyone in their lane.
					</p>

					<!-- Avatar stack -->
					<div class="mb-5 flex -space-x-2.5">
						{#each [
							{ c:'bg-violet-500/30 backdrop-blur-3xl border-violet-500/40',   t:'A' },
							{ c:'bg-emerald-500/30 backdrop-blur-3xl border-emerald-500/40', t:'M' },
							{ c:'bg-blue-500/30 backdrop-blur-3xl border-blue-500/40',       t:'S' },
							{ c:'bg-amber-500/30 backdrop-blur-3xl border-amber-500/40',     t:'+2' },
						] as av}
							<div class="flex h-7 w-7 items-center justify-center rounded-full border
                                 text-[10px] font-semibold {av.c}
                                 {isDark ? 'text-white/60' : 'text-zinc-600'}">
								{av.t}
							</div>
						{/each}
					</div>

					<!-- Role badges with icons -->
					<div class="flex flex-wrap gap-2">
						{#each [
							{
								label: 'Admin',
								delay: '0s',
								color: 'border-violet-500/20 bg-violet-500/[0.06] text-violet-400',
								icon: `<path stroke-linecap="round" stroke-linejoin="round"
                                d="M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z"/>`
							},
							{
								label: 'Manager',
								delay: '0.15s',
								color: 'border-emerald-500/20 bg-emerald-500/[0.06] text-emerald-400',
								icon: `<path stroke-linecap="round" stroke-linejoin="round"
                                d="M20.25 14.15v4.25c0 1.094-.787 2.036-1.872 2.18-2.087.277-4.216.42-6.378.42s-4.291-.143-6.378-.42c-1.085-.144-1.872-1.086-1.872-2.18v-4.25m16.5 0a2.18 2.18 0 00.75-1.661V8.706c0-1.081-.768-2.015-1.837-2.175a48.114 48.114 0 00-3.413-.387m4.5 8.006c-.194.165-.42.295-.673.38A23.978 23.978 0 0112 15.75c-2.648 0-5.195-.429-7.577-1.22a2.016 2.016 0 01-.673-.38m0 0A2.18 2.18 0 013 12.489V8.706c0-1.081.768-2.015 1.837-2.175a48.111 48.111 0 013.413-.387m7.5 0V5.25A2.25 2.25 0 0013.5 3h-3a2.25 2.25 0 00-2.25 2.25v.894m7.5 0a48.667 48.667 0 00-7.5 0M12 12.75h.008v.008H12v-.008z"/>`
							},
							{
								label: 'Accountant',
								delay: '0.3s',
								color: 'border-blue-500/20 bg-blue-500/[0.06] text-blue-400',
								icon: `<path stroke-linecap="round" stroke-linejoin="round"
                                d="M15.75 15.75V18m-7.5-6.75h.008v.008H8.25v-.008zm0 2.25h.008v.008H8.25V13.5zm0 2.25h.008v.008H8.25v-.008zm0 2.25h.008v.008H8.25V18zm2.498-6.75h.007v.008h-.007v-.008zm0 2.25h.007v.008h-.007V13.5zm0 2.25h.007v.008h-.007v-.008zm0 2.25h.007v.008h-.007V18zm2.504-6.75h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V13.5zm0 2.25h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V18zm2.498-6.75h.008v.008h-.008v-.008zm0 2.25h.008v.008h-.008V13.5zM8.25 6h7.5v2.25h-7.5V6zM12 2.25c-1.892 0-3.758.11-5.593.322C5.307 2.7 4.5 3.65 4.5 4.757V19.5a2.25 2.25 0 002.25 2.25h10.5a2.25 2.25 0 002.25-2.25V4.757c0-1.108-.806-2.057-1.907-2.185A48.507 48.507 0 0012 2.25z"/>`
							},
							{
								label: 'Sales',
								delay: '0.45s',
								color: 'border-amber-500/20 bg-amber-500/[0.06] text-amber-400',
								icon: `<path stroke-linecap="round" stroke-linejoin="round"
                                d="M2.25 18.75a60.07 60.07 0 0115.797 2.101c.727.198 1.453-.342 1.453-1.096V18.75M3.75 4.5v.75A.75.75 0 013 6h-.75m0 0v-.375c0-.621.504-1.125 1.125-1.125H20.25M2.25 6v9m18-10.5v.75c0 .414.336.75.75.75h.75m-1.5-1.5h.375c.621 0 1.125.504 1.125 1.125v9.75c0 .621-.504 1.125-1.125 1.125h-.375m1.5-1.5H21a.75.75 0 00-.75.75v.75m0 0H3.75m0 0h-.375a1.125 1.125 0 01-1.125-1.125V15m1.5 1.5v-.75A.75.75 0 003 15h-.75M15 10.5a3 3 0 11-6 0 3 3 0 016 0zm3 0h.008v.008H18V10.5zm-12 0h.008v.008H6V10.5z"/>`
							},
						] as role}
							<div
									class="flex items-center gap-2 rounded-xl border px-3 py-2 {role.color}"
									style="animation:mail-float 3.5s ease-in-out infinite;animation-delay:{role.delay};"
							>
								<svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 shrink-0"
								     fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
									{@html role.icon}
								</svg>
								<span class="text-[11px] font-medium">{role.label}</span>
							</div>
						{/each}
					</div>
				</div>
			</div>

			<!-- ══════════════════════════════════════════════════════
                 CARD 6 · Cash Flow Forecasting  (col-span-3)
                 emerald · bleeding lines · wave area chart · ascending bars
            ════════════════════════════════════════════════════════ -->
			<div
					class="group relative md:col-span-3 transition-all duration-500
                   {featuresVisible ? 'translate-y-0 opacity-100' : 'translate-y-8 opacity-0'}"
					style="transition-delay:600ms;"
			>
				<!-- Bleeding cross-lines (emerald) -->
				<div class="pointer-events-none absolute -inset-4 opacity-20 transition-opacity group-hover:opacity-45">
					<div class="absolute top-[10px] -left-[15px] h-[1px] w-[calc(100%+30px)]
                           {isDark ? 'bg-emerald-500/60' : 'bg-emerald-500/50'}"></div>
					<div class="absolute bottom-[10px] -right-[15px] h-[1px] w-[calc(100%+30px)]
                           {isDark ? 'bg-emerald-500/60' : 'bg-emerald-500/50'}"></div>
					<div class="absolute -top-[15px] left-[10px] h-[calc(100%+30px)] w-[1px]
                           {isDark ? 'bg-emerald-500/60' : 'bg-emerald-500/50'}"></div>
					<div class="absolute -bottom-[15px] right-[10px] h-[calc(100%+30px)] w-[1px]
                           {isDark ? 'bg-emerald-500/60' : 'bg-emerald-500/50'}"></div>
				</div>

				<!-- Card surface -->
				<div
						class="relative overflow-hidden rounded-2xl border p-8 h-full
                      transition-all duration-500 hover:border-emerald-500/25
                      {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'}
                      backdrop-blur-sm"
				>
					<!-- Subtle rising gradient -->
					<div class="pointer-events-none absolute bottom-0 left-0 right-0 h-1/2 opacity-[0.05]"
					     style="background:linear-gradient(to top,#10b981,transparent);
                           animation:radius-morph 13s ease-in-out infinite;">
					</div>

					<div class="relative">
						<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl
                              border border-emerald-500/20 bg-emerald-500/[0.08]">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400"
							     fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round"
								      d="M2.25 18L9 11.25l4.306 4.307a11.95 11.95 0 015.814-5.519l2.74-1.22m0 0l-5.94-2.28m5.94 2.28l-2.28 5.941"/>
							</svg>
						</div>

						<h3 class="mb-2 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">
							Cash Flow Forecasting
						</h3>
						<p class="mb-6 text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">
							AI predicts upcoming payment gaps and recommends actions before problems arise.
						</p>

						<!-- Curved line chart -->
						<div class="relative rounded-xl overflow-hidden
                              {isDark ? 'bg-black/20' : 'bg-white/70'}
                              border {isDark ? 'border-white/[0.05]' : 'border-zinc-100'}">

							<!-- Grid lines -->
							<div class="pointer-events-none absolute inset-x-0 top-3 bottom-7 flex flex-col justify-between">
								{#each [0,1,2,3] as _}
									<div class="w-full h-[1px] {isDark ? 'bg-white/[0.04]' : 'bg-zinc-200/60'}"></div>
								{/each}
							</div>

							<svg viewBox="0 0 300 82" preserveAspectRatio="none"
							     class="w-full" style="height:100px;display:block;">
								<defs>
									<linearGradient id="cf-fill" x1="0" y1="0" x2="0" y2="1">
										<stop offset="0%"   stop-color="#10b981" stop-opacity="0.22"/>
										<stop offset="100%" stop-color="#10b981" stop-opacity="0"/>
									</linearGradient>
								</defs>

								<!-- Gradient area fill -->
								<path
										d="M0,66 C30,62 45,58 65,50 C85,42 95,54 118,46
                              C140,38 150,26 170,20 C190,14 202,32 222,21
                              L222,82 L0,82 Z"
										fill="url(#cf-fill)"
										style="animation:area-pulse 4s ease-in-out infinite;"
								/>

								<!-- Solid curve (history) -->
								<path
										d="M0,66 C30,62 45,58 65,50 C85,42 95,54 118,46
                              C140,38 150,26 170,20 C190,14 202,32 222,21"
										fill="none" stroke-width="2"
										stroke-linecap="round" stroke-linejoin="round"
										class="stroke-emerald-400"
										style="animation:area-pulse 4s ease-in-out infinite;"
								/>

								<!-- Dashed forecast extension -->
								<path
										d="M222,21 C240,12 258,16 278,8 L298,4"
										fill="none" stroke-width="1.5"
										stroke-dasharray="4 3" stroke-linecap="round"
										class="stroke-emerald-400/40"
								/>

								<!-- Forecast divider -->
								<line x1="222" y1="0" x2="222" y2="82"
								      class="stroke-white/10" stroke-width="1"
								      stroke-dasharray="3 3"/>

								<!-- Data-point dots -->
								{#each [[0,66],[65,50],[118,46],[170,20],[222,21]] as [cx,cy], i}
									<!-- outer pulse ring -->
									<circle cx={cx} cy={cy} r="5"
									        class="fill-emerald-400/12"
									        style="animation:pulse-ring 2.4s ease-in-out infinite;animation-delay:{i*0.3}s;"/>
									<!-- solid dot -->
									<circle cx={cx} cy={cy} r="2.8"
									        class="fill-emerald-400 stroke-[1.5] {isDark ? 'stroke-zinc-950' : 'stroke-white'}"
									        style="animation:gen-line-in 0.4s ease-out both;animation-delay:{0.2+i*0.14}s;"/>
								{/each}

								<!-- Forecast end dot (hollow) -->
								<circle cx="298" cy="4" r="2.8"
								        class="fill-transparent stroke-emerald-400/50" stroke-width="1.5"
								/>
							</svg>

							<!-- Month labels -->
							<div class="flex justify-between px-3 pb-2 -mt-1"
							     style="font-family:'DM Sans',sans-serif;">
								{#each ['Jan','Feb','Mar','Apr','May','Jun'] as m}
									<span class="text-[9px] {isDark ? 'text-white/20' : 'text-zinc-400'}">{m}</span>
								{/each}
							</div>

							<!-- Forecast label chip -->
							<div class="absolute top-3 right-3 flex items-center gap-1.5 rounded-md border px-2 py-1
                                 {isDark ? 'border-white/[0.06] bg-white/[0.03]' : 'border-zinc-100 bg-white/80'}">
								<div class="h-[1px] w-4" style="background:repeating-linear-gradient(to right,rgb(52 211 153/0.5) 0,rgb(52 211 153/0.5) 3px,transparent 3px,transparent 6px);"></div>
								<span class="text-[9px] {isDark ? 'text-white/25' : 'text-zinc-400'}">forecast</span>
							</div>
						</div>
					</div>

					<!-- Bottom wave -->
					<div class="pointer-events-none absolute bottom-0 left-0 right-0 h-10 overflow-hidden
                           {isDark ? 'opacity-[0.04]' : 'opacity-[0.05]'}">
						<svg class="absolute bottom-0 text-emerald-400"
						     style="width:200%;animation:wave-flow 9s linear infinite;"
						     viewBox="0 0 1440 40" preserveAspectRatio="none" fill="currentColor">
							<path d="M0,20 C120,34 240,6 360,20 C480,34 600,6 720,20
                              C840,34 960,6 1080,20 C1200,34 1320,6 1440,20
                              C1560,34 1680,6 1800,20 C1920,34 2040,6 2160,20
                              C2280,34 2400,6 2520,20 C2640,34 2760,6 2880,20 L2880,40 L0,40 Z"/>
						</svg>
					</div>
				</div>
			</div>

		</div>
	</div>
</section>

<style>
	/* ── Wave ── */
	@keyframes wave-flow {
		0%   { transform: translateX(0); }
		100% { transform: translateX(-50%); }
	}

	/* ── Border-radius morph (for glow blobs & accent elements) ── */
	@keyframes radius-morph {
		0%, 100% { border-radius: 40% 60% 60% 40% / 60% 40% 60% 40%; }
		25%       { border-radius: 60% 40% 30% 70% / 50% 60% 40% 50%; }
		50%       { border-radius: 30% 70% 70% 30% / 30% 50% 50% 70%; }
		75%       { border-radius: 70% 30% 40% 60% / 60% 40% 30% 40%; }
	}

	/* ── Area chart pulse ── */
	@keyframes area-pulse {
		0%, 100% { opacity: 1; }
		50%       { opacity: 0.6; }
	}

	/* ── Generation scan beam ── */
	@keyframes gen-scan {
		0%   { transform: translateX(-100%); }
		100% { transform: translateX(450%); }
	}

	/* ── Line reveal (generation) ── */
	@keyframes gen-line-in {
		0%   { opacity: 0; transform: translateY(4px); }
		100% { opacity: 1; transform: translateY(0); }
	}

	/* ── Existing animations (re-declared for self-containment) ── */
	@keyframes mail-float {
		0%, 100% { transform: translateY(0px);   opacity: 0.15; }
		50%       { transform: translateY(-10px); opacity: 0.4;  }
	}
	@keyframes pulse-dot {
		0%, 100% { opacity: 0.3; transform: scale(1);   }
		50%       { opacity: 0.8; transform: scale(1.3); }
	}
	@keyframes ring-expand {
		0%   { transform: translate(-50%,-50%) scale(0.5); opacity: 0.4; }
		100% { transform: translate(-50%,-50%) scale(1.8); opacity: 0;   }
	}
	@keyframes bell-ring {
		0%, 80%, 100% { transform: rotate(0deg);   }
		5%             { transform: rotate(12deg);  }
		10%            { transform: rotate(-10deg); }
		15%            { transform: rotate(8deg);   }
		20%            { transform: rotate(-5deg);  }
		25%            { transform: rotate(0deg);   }
	}
	@keyframes bar-breathe {
		0%, 100% { transform: scaleY(1);   }
		50%       { transform: scaleY(1.4); }
	}
	@keyframes bar-grow {
		0%   { transform: scaleY(0); opacity: 0; }
		100% { transform: scaleY(1); opacity: 1; }
	}
	@keyframes cursor-blink {
		0%, 100% { opacity: 1; }
		50%       { opacity: 0; }
	}
	@keyframes pulse-ring {
		0%, 100% { r: 5;   opacity: 0.12; }
		50%       { r: 7.5; opacity: 0.22; }
	}

	/* ── Global dot grid animations (shared via :global) ── */
	:global(.ai-dots) {
		animation: ai-dots-drift 40s linear infinite;
	}
	@keyframes ai-dots-drift {
		0%   { transform: translate(0, 0);     }
		50%  { transform: translate(8px, 8px); }
		100% { transform: translate(0, 0);     }
	}
	:global(.team-dots) {
		animation: team-dots-drift 28s linear infinite reverse;
	}
	@keyframes team-dots-drift {
		0%   { transform: translate(0, 0);       }
		100% { transform: translate(14px, 14px); }
	}
</style>
