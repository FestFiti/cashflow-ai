import { writable } from 'svelte/store';
import { browser } from '$app/environment';

interface AuthState {
	token: string | null;
	businessId: string | null;
	name: string | null;
}

const stored = browser ? localStorage.getItem('auth') : null;
const initial: AuthState = stored
	? JSON.parse(stored)
	: { token: null, businessId: null, name: null };

export const auth = writable<AuthState>(initial);

auth.subscribe((value) => {
	if (browser) {
		localStorage.setItem('auth', JSON.stringify(value));
	}
});

export function login(token: string, businessId: string, name: string) {
	auth.set({ token, businessId, name });
}

export function logout() {
	auth.set({ token: null, businessId: null, name: null });
}
