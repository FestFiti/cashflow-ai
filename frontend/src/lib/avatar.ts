export function getAvatarUrl(seed: string, size = 64): string {
	return `https://api.dicebear.com/9.x/identicon/svg?seed=${encodeURIComponent(seed)}&size=${size}`;
}
