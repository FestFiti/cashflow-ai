<script lang="ts">

	interface Props {
		isDark: boolean;
	}

	let { isDark }: Props = $props();
</script>

<!-- FOOTER -->
<footer class="border-t py-12 transition-colors {isDark ? 'border-white/[0.04] bg-zinc-950' : 'border-zinc-200 bg-white'}">
	<div class="mx-auto max-w-7xl px-6" style="font-family: 'DM Sans', sans-serif;">
		<div class="grid grid-cols-1 gap-8 md:grid-cols-4">
			<div>
				<div class="mb-4 flex items-center gap-2.5">
					<img src={isDark ? '/logo-gold.png' : '/logo-dark.png'} alt="CashFlow AI" class="h-8 w-8" />
					<span class="text-[14px] font-semibold {isDark ? 'text-white/80' : 'text-zinc-800'}">CashFlow AI</span>
				</div>
				<p class="text-[13px] leading-relaxed {isDark ? 'text-white/25' : 'text-zinc-400'}">
					Intelligent payment orchestration for African businesses.
				</p>
			</div>
			<div>
				<h4 class="mb-4 text-[11px] font-semibold uppercase tracking-[0.15em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Product</h4>
				<ul class="space-y-2.5 text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'}">
					<li><a href="#features" class="transition-colors {isDark ? 'hover:text-white/80' : 'hover:text-zinc-900'}">Features</a></li>
					<li><a href="#how-it-works" class="transition-colors {isDark ? 'hover:text-white/80' : 'hover:text-zinc-900'}">How It Works</a></li>
					<li><a href="/register" class="transition-colors {isDark ? 'hover:text-white/80' : 'hover:text-zinc-900'}">Get Started</a></li>
				</ul>
			</div>
			<div>
				<h4 class="mb-4 text-[11px] font-semibold uppercase tracking-[0.15em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Integrations</h4>
				<ul class="space-y-2.5 text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'}">
					<li>M-Pesa Daraja</li>
					<li>Ratiba</li>
					<li>AI Engine</li>
				</ul>
			</div>
			<div>
				<h4 class="mb-4 text-[11px] font-semibold uppercase tracking-[0.15em] {isDark ? 'text-white/25' : 'text-zinc-400'}">Support</h4>
				<ul class="space-y-2.5 text-[13px] {isDark ? 'text-white/40' : 'text-zinc-500'}">
					<li><a href="/docs" class="transition-colors {isDark ? 'hover:text-white/80' : 'hover:text-zinc-900'}">Documentation</a></li>
					<li><a href="/docs" class="transition-colors {isDark ? 'hover:text-white/80' : 'hover:text-zinc-900'}">API Reference</a></li>
				</ul>
			</div>
		</div>
		<div class="mt-10 border-t pt-6 text-center text-[12px] {isDark ? 'border-white/[0.04] text-white/15' : 'border-zinc-200 text-zinc-400'}">
			2026 CashFlow AI by Gatekeepers Group. Built for African businesses.
		</div>
	</div>
</footer>
