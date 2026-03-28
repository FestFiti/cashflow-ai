const API_URL = import.meta.env.PUBLIC_API_URL || 'http://localhost:8888';

interface FetchOptions extends RequestInit {
	token?: string;
}

export async function api<T>(path: string, options: FetchOptions = {}): Promise<T> {
	const { token, ...fetchOptions } = options;

	const headers: Record<string, string> = {
		'Content-Type': 'application/json',
		...(options.headers as Record<string, string>)
	};

	if (token) {
		headers['Authorization'] = `Bearer ${token}`;
	}

	const res = await fetch(`${API_URL}${path}`, {
		...fetchOptions,
		headers
	});

	if (!res.ok) {
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
