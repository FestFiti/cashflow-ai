<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import * as THREE from 'three';

	let container: HTMLDivElement;
	let animationId: number;

	onMount(() => {
		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 100);
		camera.position.z = 4;

		const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
		renderer.setSize(container.clientWidth, container.clientHeight);
		renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
		renderer.toneMapping = THREE.ACESFilmicToneMapping;
		renderer.toneMappingExposure = 1.2;
		container.appendChild(renderer.domElement);

		// Iridescent metallic blob geometry
		const geometry = new THREE.IcosahedronGeometry(1.4, 64);
		const positionAttr = geometry.attributes.position;
		const originalPositions = new Float32Array(positionAttr.array);

		// Custom shader material for metallic iridescent look
		const material = new THREE.ShaderMaterial({
			uniforms: {
				uTime: { value: 0 },
				uColor1: { value: new THREE.Color('#10b981') },
				uColor2: { value: new THREE.Color('#064e3b') },
				uColor3: { value: new THREE.Color('#d4a574') },
				uLightPos: { value: new THREE.Vector3(2, 3, 4) }
			},
			vertexShader: `
				uniform float uTime;
				varying vec3 vNormal;
				varying vec3 vPosition;
				varying float vDisplacement;

				// Simplex noise approximation
				vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
				vec4 mod289(vec4 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
				vec4 permute(vec4 x) { return mod289(((x * 34.0) + 1.0) * x); }
				vec4 taylorInvSqrt(vec4 r) { return 1.79284291400159 - 0.85373472095314 * r; }

				float snoise(vec3 v) {
					const vec2 C = vec2(1.0/6.0, 1.0/3.0);
					const vec4 D = vec4(0.0, 0.5, 1.0, 2.0);
					vec3 i = floor(v + dot(v, C.yyy));
					vec3 x0 = v - i + dot(i, C.xxx);
					vec3 g = step(x0.yzx, x0.xyz);
					vec3 l = 1.0 - g;
					vec3 i1 = min(g.xyz, l.zxy);
					vec3 i2 = max(g.xyz, l.zxy);
					vec3 x1 = x0 - i1 + C.xxx;
					vec3 x2 = x0 - i2 + C.yyy;
					vec3 x3 = x0 - D.yyy;
					i = mod289(i);
					vec4 p = permute(permute(permute(
						i.z + vec4(0.0, i1.z, i2.z, 1.0))
						+ i.y + vec4(0.0, i1.y, i2.y, 1.0))
						+ i.x + vec4(0.0, i1.x, i2.x, 1.0));
					float n_ = 0.142857142857;
					vec3 ns = n_ * D.wyz - D.xzx;
					vec4 j = p - 49.0 * floor(p * ns.z * ns.z);
					vec4 x_ = floor(j * ns.z);
					vec4 y_ = floor(j - 7.0 * x_);
					vec4 x = x_ * ns.x + ns.yyyy;
					vec4 y = y_ * ns.x + ns.yyyy;
					vec4 h = 1.0 - abs(x) - abs(y);
					vec4 b0 = vec4(x.xy, y.xy);
					vec4 b1 = vec4(x.zw, y.zw);
					vec4 s0 = floor(b0) * 2.0 + 1.0;
					vec4 s1 = floor(b1) * 2.0 + 1.0;
					vec4 sh = -step(h, vec4(0.0));
					vec4 a0 = b0.xzyw + s0.xzyw * sh.xxyy;
					vec4 a1 = b1.xzyw + s1.xzyw * sh.zzww;
					vec3 p0 = vec3(a0.xy, h.x);
					vec3 p1 = vec3(a0.zw, h.y);
					vec3 p2 = vec3(a1.xy, h.z);
					vec3 p3 = vec3(a1.zw, h.w);
					vec4 norm = taylorInvSqrt(vec4(dot(p0,p0), dot(p1,p1), dot(p2,p2), dot(p3,p3)));
					p0 *= norm.x; p1 *= norm.y; p2 *= norm.z; p3 *= norm.w;
					vec4 m = max(0.6 - vec4(dot(x0,x0), dot(x1,x1), dot(x2,x2), dot(x3,x3)), 0.0);
					m = m * m;
					return 42.0 * dot(m*m, vec4(dot(p0,x0), dot(p1,x1), dot(p2,x2), dot(p3,x3)));
				}

				void main() {
					float noise = snoise(position * 1.5 + uTime * 0.3) * 0.15;
					noise += snoise(position * 3.0 + uTime * 0.5) * 0.08;
					vec3 newPosition = position + normal * noise;
					vDisplacement = noise;
					vNormal = normalize(normalMatrix * normal);
					vPosition = (modelViewMatrix * vec4(newPosition, 1.0)).xyz;
					gl_Position = projectionMatrix * modelViewMatrix * vec4(newPosition, 1.0);
				}
			`,
			fragmentShader: `
				uniform vec3 uColor1;
				uniform vec3 uColor2;
				uniform vec3 uColor3;
				uniform vec3 uLightPos;
				uniform float uTime;
				varying vec3 vNormal;
				varying vec3 vPosition;
				varying float vDisplacement;

				void main() {
					vec3 lightDir = normalize(uLightPos - vPosition);
					vec3 viewDir = normalize(-vPosition);
					vec3 halfDir = normalize(lightDir + viewDir);

					// Fresnel effect for iridescence
					float fresnel = pow(1.0 - max(dot(viewDir, vNormal), 0.0), 3.0);

					// Diffuse + specular
					float diff = max(dot(vNormal, lightDir), 0.0);
					float spec = pow(max(dot(vNormal, halfDir), 0.0), 64.0);

					// Color mixing based on normal angle and displacement
					float colorMix = vNormal.y * 0.5 + 0.5;
					vec3 baseColor = mix(uColor2, uColor1, colorMix);
					baseColor = mix(baseColor, uColor3, fresnel * 0.7);

					// Ambient occlusion from displacement
					float ao = smoothstep(-0.15, 0.15, vDisplacement) * 0.4 + 0.6;

					vec3 ambient = baseColor * 0.15 * ao;
					vec3 diffuse = baseColor * diff * 0.6;
					vec3 specular = vec3(1.0, 0.95, 0.85) * spec * 1.2;
					vec3 rim = uColor1 * fresnel * 0.4;

					vec3 finalColor = ambient + diffuse + specular + rim;

					// Tone mapping
					finalColor = finalColor / (finalColor + vec3(1.0));

					gl_FragColor = vec4(finalColor, 0.95);
				}
			`,
			transparent: true,
		});

		const mesh = new THREE.Mesh(geometry, material);
		mesh.position.y = -0.2;
		scene.add(mesh);

		// Subtle ambient particles
		const particleCount = 60;
		const particleGeometry = new THREE.BufferGeometry();
		const particlePositions = new Float32Array(particleCount * 3);
		for (let i = 0; i < particleCount; i++) {
			particlePositions[i * 3] = (Math.random() - 0.5) * 8;
			particlePositions[i * 3 + 1] = (Math.random() - 0.5) * 6;
			particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 4 - 2;
		}
		particleGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
		const particleMaterial = new THREE.PointsMaterial({
			size: 0.015,
			color: 0x10b981,
			transparent: true,
			opacity: 0.4,
			sizeAttenuation: true
		});
		const particles = new THREE.Points(particleGeometry, particleMaterial);
		scene.add(particles);

		let mouseX = 0, mouseY = 0;
		const handleMouseMove = (e: MouseEvent) => {
			mouseX = (e.clientX / window.innerWidth - 0.5) * 2;
			mouseY = (e.clientY / window.innerHeight - 0.5) * 2;
		};
		window.addEventListener('mousemove', handleMouseMove);

		const clock = new THREE.Clock();

		function animate() {
			animationId = requestAnimationFrame(animate);
			const t = clock.getElapsedTime();

			material.uniforms.uTime.value = t;

			mesh.rotation.x += (mouseY * 0.1 - mesh.rotation.x) * 0.02;
			mesh.rotation.y += (mouseX * 0.2 - mesh.rotation.y) * 0.02;

			particles.rotation.y = t * 0.02;
			particles.rotation.x = t * 0.01;

			renderer.render(scene, camera);
		}
		animate();

		const handleResize = () => {
			const w = container.clientWidth;
			const h = container.clientHeight;
			camera.aspect = w / h;
			camera.updateProjectionMatrix();
			renderer.setSize(w, h);
		};
		window.addEventListener('resize', handleResize);

		return () => {
			cancelAnimationFrame(animationId);
			window.removeEventListener('mousemove', handleMouseMove);
			window.removeEventListener('resize', handleResize);
			renderer.dispose();
			geometry.dispose();
			material.dispose();
			particleGeometry.dispose();
			particleMaterial.dispose();
			if (container?.contains(renderer.domElement)) {
				container.removeChild(renderer.domElement);
			}
		};
	});
</script>

<div bind:this={container} class="absolute inset-0 z-0"></div>
