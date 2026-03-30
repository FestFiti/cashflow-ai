<script lang="ts">

	interface Props {
		isDark: boolean;
	}

	let { isDark }: Props = $props();
</script>

<!-- INTEGRATIONS — Bento Grid -->
<section id="integrations" class="relative py-28 transition-colors {isDark ? 'bg-zinc-950' : 'bg-white'}">
	<!-- Section dot grid background -->
	<div class="pointer-events-none absolute inset-0 {isDark ? 'opacity-[0.015]' : 'opacity-[0.04]'}" style="background-image: radial-gradient(circle, {isDark ? 'white' : '#a1a1aa'} 0.5px, transparent 0.5px); background-size: 20px 20px;"></div>

	<div class="relative mx-auto max-w-7xl px-6">
		<div class="mb-16 text-center">
			<p class="mb-3 text-[12px] font-semibold uppercase tracking-[0.2em] text-emerald-500" style="font-family: 'DM Sans', sans-serif;">Integrations</p>
			<h2 class="font-['Instrument_Serif'] text-4xl tracking-tight md:text-5xl {isDark ? 'text-white' : 'text-zinc-900'}">
				Powered by <span class="italic text-emerald-400">trusted</span> APIs
			</h2>
		</div>

		<!-- Bento layout -->
		<div class="grid grid-cols-1 gap-4 md:grid-cols-6" style="font-family: 'DM Sans', sans-serif;">

			<!-- M-Pesa — wide card with animated grid texture -->
			<div class="group relative overflow-hidden rounded-2xl border md:col-span-4 {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'} transition-all hover:border-emerald-500/20">
				<!-- Animated sliding grid -->
				<div class="mpesa-grid pointer-events-none absolute -inset-20 {isDark ? 'opacity-[0.04]' : 'opacity-[0.07]'}" style="background-image: linear-gradient({isDark ? 'rgba(16,185,129,0.4)' : 'rgba(16,185,129,0.3)'} 1px, transparent 1px), linear-gradient(90deg, {isDark ? 'rgba(16,185,129,0.4)' : 'rgba(16,185,129,0.3)'} 1px, transparent 1px); background-size: 40px 40px;"></div>
				<div class="absolute -right-10 -top-10 h-52 w-52 rounded-full opacity-[0.06]" style="background: radial-gradient(circle, #10b981 0%, transparent 70%);"></div>
				<div class="relative p-8">
					<div class="mb-5 flex items-center gap-3">
						<div class="flex h-12 w-12 items-center justify-center rounded-xl border border-emerald-500/20 bg-emerald-500/[0.08]">
							<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
								<path stroke-linecap="round" stroke-linejoin="round" d="M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3" />
							</svg>
						</div>
						<div>
							<h3 class="text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">M-Pesa Daraja</h3>
							<p class="text-[11px] {isDark ? 'text-white/25' : 'text-zinc-400'}">Payment Infrastructure</p>
						</div>
					</div>
					<p class="mb-6 max-w-sm text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">Complete payment orchestration from customer to business and back.</p>
					<!-- Icon tags -->
					<div class="flex flex-wrap gap-2">
						{#each [
							{ label: 'STK Push', d: 'M10.5 1.5H8.25A2.25 2.25 0 006 3.75v16.5a2.25 2.25 0 002.25 2.25h7.5A2.25 2.25 0 0018 20.25V3.75a2.25 2.25 0 00-2.25-2.25H13.5m-3 0V3h3V1.5m-3 0h3m-3 18.75h3' },
							{ label: 'B2C', d: 'M6 12L3.269 3.126A59.768 59.768 0 0121.485 12 59.77 59.77 0 013.27 20.876L5.999 12zm0 0h7.5' },
							{ label: 'C2B', d: 'M9 3.75H6.912a2.25 2.25 0 00-2.15 1.588L2.35 13.177a2.25 2.25 0 00-.1.661V18a2.25 2.25 0 002.25 2.25h15A2.25 2.25 0 0021.75 18v-4.162c0-.224-.034-.447-.1-.661L19.24 5.338a2.25 2.25 0 00-2.15-1.588H15M2.25 13.5h3.86a2.25 2.25 0 012.012 1.244l.256.512a2.25 2.25 0 002.013 1.244h3.218a2.25 2.25 0 002.013-1.244l.256-.512a2.25 2.25 0 012.013-1.244h3.859' },
							{ label: 'Reversal', d: 'M9 15L3 9m0 0l6-6M3 9h12a6 6 0 010 12h-3' },
							{ label: 'Status', d: 'M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z' }
						] as tag}
							<span class="inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-[11px] font-medium transition-colors group-hover:border-emerald-500/30 {isDark ? 'border-white/[0.06] bg-white/[0.02] text-emerald-400/80' : 'border-zinc-200 bg-white text-emerald-700'}">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
									<path stroke-linecap="round" stroke-linejoin="round" d={tag.d} />
								</svg>
								{tag.label}
							</span>
						{/each}
					</div>
				</div>
			</div>

			<!-- Cash Flow AI — tall card with animated dot grid bleeding outside -->
			<div class="group relative md:col-span-2 md:row-span-2">
				<!-- Animated outer dots bleeding beyond the card -->
								<!-- Bleeding corner lines -->
								<div class="pointer-events-none absolute -inset-4 opacity-20 transition-opacity group-hover:opacity-40">
									<!-- Top line -->
									<div class="absolute top-[10px] -left-[15px] h-[1px] w-[calc(100%+30px)] {isDark ? 'bg-violet-500/50' : 'bg-violet-500'}"></div>
									<!-- Bottom line -->
									<div class="absolute bottom-[10px] -right-[15px] h-[1px] w-[calc(100%+30px)] {isDark ? 'bg-violet-500/50' : 'bg-violet-500'}"></div>
									<!-- Left line -->
									<div class="absolute -top-[15px] left-[10px] h-[calc(100%+30px)] w-[1px] {isDark ? 'bg-violet-500/50' : 'bg-violet-500'}"></div>
									<!-- Right line -->
									<div class="absolute -bottom-[15px] right-[10px] h-[calc(100%+30px)] w-[1px] {isDark ? 'bg-violet-500/50' : 'bg-violet-500'}"></div>
								</div><div class="ai-dots pointer-events-none absolute -inset-6 {isDark ? 'opacity-[0.05]' : 'opacity-[0.1]'}" style="background-image: radial-gradient(circle, {isDark ? '#8b5cf6' : '#7c3aed'} 1.5px, transparent 1.5px); background-size: 16px 16px;"></div>
				<div class="relative h-full overflow-hidden rounded-2xl border {isDark ? 'border-white/[0.04] bg-zinc-950/80' : 'border-zinc-200 bg-white'} backdrop-blur-sm transition-all hover:border-violet-500/20">
					<div class="absolute -right-16 -bottom-16 h-56 w-56 rounded-full opacity-[0.06]" style="background: radial-gradient(circle, #8b5cf6 0%, transparent 60%);"></div>
					<div class="relative flex h-full flex-col p-8">
						<div class="mb-auto">
							<div class="mb-6 flex h-12 w-12 items-center justify-center rounded-xl border border-violet-500/20 bg-violet-500/[0.08]">
								<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-violet-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
									<path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
						</svg>
							</div>
							<h3 class="mb-1 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">Cash Flow AI</h3>
							<p class="mb-4 text-[11px] {isDark ? 'text-white/25' : 'text-zinc-400'}">Intelligence Layer</p>
							<p class="text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">Natural language invoice parsing, personalised reminder drafting, and predictive cash flow insights.</p>
						</div>
						<!-- Decorative waveform -->
						<div class="mt-8 flex items-end gap-[3px]">
							{#each Array(16) as _, j}
								<div
									class="w-1.5 rounded-full bg-violet-500/40"
									style="height: {8 + Math.sin(j * 0.8) * 12 + Math.random() * 4}px; animation: bar-breathe {1.2 + (j % 5) * 0.3}s ease-in-out infinite; animation-delay: {j * 0.1}s;"
								></div>
							{/each}
						</div>
					</div>
				</div>
			</div>

			<!-- Ratiba — with animated diagonal lines texture -->
			<div class="group relative overflow-hidden rounded-2xl border md:col-span-2 {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'} transition-all hover:border-blue-500/20">
				<div class="ratiba-stripes pointer-events-none absolute -inset-10 {isDark ? 'opacity-[0.03]' : 'opacity-[0.05]'}" style="background-image: repeating-linear-gradient(45deg, {isDark ? 'rgba(59,130,246,0.5)' : 'rgba(59,130,246,0.4)'} 0px, {isDark ? 'rgba(59,130,246,0.5)' : 'rgba(59,130,246,0.4)'} 1px, transparent 1px, transparent 12px);"></div>
				<div class="relative p-8">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-blue-500/20 bg-blue-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M12 6v6h4.5m4.5 0a9 9 0 11-18 0 9 9 0 0118 0z" />
						</svg>
					</div>
					<h3 class="mb-1 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">Ratiba</h3>
					<p class="mb-3 text-[11px] {isDark ? 'text-white/25' : 'text-zinc-400'}">Scheduling Engine</p>
					<p class="text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">Scheduled reminders, recurring invoice automation, and webhook-driven status updates.</p>
					<!-- Animated timeline -->
					<div class="mt-5 flex items-center gap-2">
						{#each Array(4) as _, k}
							<div class="relative h-1 flex-1 overflow-hidden rounded-full {isDark ? 'bg-white/[0.04]' : 'bg-zinc-200'}">
								<div class="timeline-fill absolute inset-y-0 left-0 rounded-full bg-blue-500/60" style="animation-delay: {k * 0.6}s;"></div>
							</div>
						{/each}
						<div class="flex h-5 w-5 items-center justify-center rounded-full bg-blue-500/20">
							<div class="h-1.5 w-1.5 rounded-full bg-blue-400" style="animation: pulse-dot 2s ease-in-out infinite;"></div>
						</div>
					</div>
				</div>
			</div>

			<!-- Cash Flow Mail — with animated floating dots -->
			<div class="group relative overflow-hidden rounded-2xl border md:col-span-2 {isDark ? 'border-white/[0.04] bg-white/[0.02]' : 'border-zinc-200 bg-zinc-50'} transition-all hover:border-amber-500/20">
				<!-- Animated floating dots -->
				<div class="pointer-events-none absolute inset-0 overflow-hidden">
					{#each [
						{ x: 75, y: 20, s: 4, d: 3.5 },
						{ x: 85, y: 45, s: 3, d: 4.2 },
						{ x: 65, y: 65, s: 5, d: 3.0 },
						{ x: 90, y: 75, s: 3, d: 5.0 },
						{ x: 55, y: 35, s: 2, d: 3.8 },
						{ x: 80, y: 85, s: 4, d: 4.5 },
						{ x: 70, y: 50, s: 2, d: 3.2 },
						{ x: 60, y: 80, s: 3, d: 4.8 },
						{ x: 92, y: 30, s: 2, d: 3.6 },
						{ x: 50, y: 55, s: 3, d: 4.0 },
					] as dot}
						<div
							class="mail-dot absolute rounded-full {isDark ? 'bg-amber-400' : 'bg-amber-500'}"
							style="left: {dot.x}%; top: {dot.y}%; width: {dot.s}px; height: {dot.s}px; animation: mail-float {dot.d}s ease-in-out infinite; animation-delay: {dot.d * 0.3}s;"
						></div>
					{/each}
				</div>
				<div class="relative p-8">
					<div class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl border border-amber-500/20 bg-amber-500/[0.08]">
						<svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
							<path stroke-linecap="round" stroke-linejoin="round" d="M21.75 6.75v10.5a2.25 2.25 0 01-2.25 2.25h-15a2.25 2.25 0 01-2.25-2.25V6.75m19.5 0A2.25 2.25 0 0019.5 4.5h-15a2.25 2.25 0 00-2.25 2.25m19.5 0v.243a2.25 2.25 0 01-1.07 1.916l-7.5 4.615a2.25 2.25 0 01-2.36 0L3.32 8.91a2.25 2.25 0 01-1.07-1.916V6.75" />
						</svg>
					</div>
					<h3 class="mb-1 text-[17px] font-semibold {isDark ? 'text-white/90' : 'text-zinc-900'}">Cash Flow Mail</h3>
					<p class="mb-3 text-[11px] {isDark ? 'text-white/25' : 'text-zinc-400'}">Transactional Email</p>
					<p class="text-[14px] leading-relaxed {isDark ? 'text-white/40' : 'text-zinc-500'}">Login alerts, password resets, invoice notifications, and payment receipts delivered instantly.</p>
				</div>
			</div>
		</div>
	</div>
</section>
