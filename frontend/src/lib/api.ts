import { get } from 'svelte/store';
import { browser } from '$app/environment';
import { auth, logout } from '$lib/stores/auth';

const API_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:8888';

interface FetchOptions extends RequestInit {
	token?: string;
}

export async function api<T>(path: string, options: FetchOptions = {}): Promise<T> {
	const { token, ...fetchOptions } = options;

	// Auto-inject token from store if not explicitly provided
	const authToken = token ?? (browser ? get(auth).token : null);

	const headers: Record<string, string> = {
		'Content-Type': 'application/json',
		...(options.headers as Record<string, string>)
	};

	if (authToken) {
		headers['Authorization'] = `Bearer ${authToken}`;
	}

	const res = await fetch(`${API_URL}${path}`, {
		...fetchOptions,
		headers
	});

	if (!res.ok) {
		// Auto-logout on 401 (expired/invalid token)
		if (res.status === 401 && browser) {
			logout();
			window.location.href = `/login?redirect=${encodeURIComponent(window.location.pathname)}`;
			throw new Error('Session expired. Please sign in again.');
		}

		const error = await res.json().catch(() => ({ detail: 'Request failed' }));
		throw new Error(error.detail || `HTTP ${res.status}`);
	}

	return res.json();
}

export function formatKES(amount: number): string {
	return new Intl.NumberFormat('en-KE', {
		style: 'currency',
		currency: 'KES',
		minimumFractionDigits: 0,
		maximumFractionDigits: 0
	}).format(amount);
}
