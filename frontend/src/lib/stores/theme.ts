import { writable } from 'svelte/store';
import { browser } from '$app/environment';

type Theme = 'dark' | 'light';

function getInitialTheme(): Theme {
	if (!browser) return 'dark';
	const stored = localStorage.getItem('theme');
	if (stored === 'light' || stored === 'dark') return stored;
	return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
}

export const theme = writable<Theme>(getInitialTheme());

theme.subscribe((value) => {
	if (!browser) return;
	localStorage.setItem('theme', value);
	document.documentElement.classList.toggle('dark', value === 'dark');
	document.documentElement.classList.toggle('light', value === 'light');
});

export function toggleTheme() {
	theme.update((t) => (t === 'dark' ? 'light' : 'dark'));
}
