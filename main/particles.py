import pygame
from support import import_folder
from random import choice

class AnimationPlayer:
	def __init__(self):
		#动画效果在这里导入
		self.frames = {
			# 魔法特效
			'flame': import_folder('../assets/graphics/particles/flame/frames'),
			'aura': import_folder('../assets/graphics/particles/aura'),
			'heal': import_folder('../assets/graphics/particles/heal/frames'),
			
			# 攻击特效
			'claw': import_folder('../assets/graphics/particles/claw'),
			'slash': import_folder('../assets/graphics/particles/slash'),
			'sparkle': import_folder('../assets/graphics/particles/sparkle'),
			'leaf_attack': import_folder('../assets/graphics/particles/leaf_attack'),
			'thunder': import_folder('../assets/graphics/particles/thunder'),

			#怪物死亡
			'Papyrus': import_folder('../assets/graphics/particles/smoke_orange'),
			'Undyne': import_folder('../assets/graphics/particles/Undyne'),
			'TEMMIE': import_folder('../assets/graphics/particles/nova'),
			'Flowey': import_folder('../assets/graphics/particles/Flowey'),
			
			# 叶子
			'leaf': (
				import_folder('../assets/graphics/particles/leaf1'),
				import_folder('../assets/graphics/particles/leaf2'),
				import_folder('../assets/graphics/particles/leaf3'),
				import_folder('../assets/graphics/particles/leaf4'),
				import_folder('../assets/graphics/particles/leaf5'),
				import_folder('../assets/graphics/particles/leaf6'),
				self.reflect_images(import_folder('../assets/graphics/particles/leaf1')),
				self.reflect_images(import_folder('../assets/graphics/particles/leaf2')),
				self.reflect_images(import_folder('../assets/graphics/particles/leaf3')),
				self.reflect_images(import_folder('../assets/graphics/particles/leaf4')),
				self.reflect_images(import_folder('../assets/graphics/particles/leaf5')),
				self.reflect_images(import_folder('../assets/graphics/particles/leaf6'))
				)
			}
	
	def reflect_images(self,frames):
		new_frames = []

		for frame in frames:
			flipped_frame = pygame.transform.flip(frame,True,False)#用于翻转图像
			new_frames.append(flipped_frame)
		return new_frames

	def create_grass_particles(self,pos,groups):
		animation_frames = choice(self.frames['leaf'])
		ParticleEffect(pos,animation_frames,groups)

	def create_particles(self,animation_type,pos,groups):
		animation_frames = self.frames[animation_type]#供选择要使用的动画图像
		ParticleEffect(pos,animation_frames,groups)


class ParticleEffect(pygame.sprite.Sprite):
	def __init__(self,pos,animation_frames,groups):
		super().__init__(groups)
		self.sprite_type = 'magic'#魔法特效
		self.frame_index = 0
		self.frames = animation_frames
		self.image = self.frames[self.frame_index]
		self.rect = self.image.get_rect(center = pos)

	def animate(self,dt):
		self.frame_index += 8*dt
		if self.frame_index >= len(self.frames):
			self.kill()#如果索引超出了范围就从组分里面删去不在更新
		else:
			self.image = self.frames[int(self.frame_index)]

	def update(self,dt):
		self.animate(dt)
