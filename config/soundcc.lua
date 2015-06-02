Sound = {
	-- Door

	door			= {
		open		= "cc/door-open",
		close		= "cc/door-close",
	},

	-- Teleport

	teleport = {
		use			= "cc/teleport",
	},

	-- default sounds
	explode = "cc/explode",
	fire = "cc/gunfire",

	-- Player
	soldier = {
		-- turns out nothing here works except for:
		--  melee hit die phase
		-- so we can't use it as a TICK function :(
	},

	-- Creatures

	former = {
		die = "cc/former/die",
		act = "cc/former/act",
		hit = "cc/former/pain",
	},

	sergeant = {
		die			= "cc/former/die-sergeant",
		act			= "cc/former/act",
		hit			= "cc/former/pain",
	},

	-- Former Captain

	captain = {
		die			= "cc/former/die-captain",
		act			= "cc/former/act",
		hit			= "cc/former/pain",
	},

	-- Former Commando

	commando = {
		die			= "cc/former/die-commando",
		act			= "cc/former/act",
		hit			= "cc/former/pain",
	},

	--[[
	--
	-- Creatures
	--

	-- Former Human

	-- Former Sergeant


	-- Imp

	imp = {
		die			= "wavhq/dsbgdth1.wav",
		act			= "wavhq/dsbgact.wav",
		hit			= "wavhq/dspopain.wav",
		melee		= "wavhq/dsclaw.wav",
		fire		= "wavhq/dsfirsht.wav",
		explode		= "wavhq/dsfirxpl.wav",
	--	hoof		= "wavhq/dshoof.wav";
	},

	-- Lost Soul

	lostsoul = {
		die			= "wavhq/dsfirxpl.wav",
		act			= "wavhq/dssklatk.wav",
		hit			= "wavhq/dsdmpain.wav",
		melee		= "wavhq/dssklatk.wav",
	},

	-- Pain Elemental

	pain = {
		die			= "wavhq/dspedth.wav",
		act			= "wavhq/dspesit.wav",
		hit			= "wavhq/dspepain.wav",
		melee		= "wavhq/dsclaw.wav";
	},

	-- Demon

	demon = {
		die			= "wavhq/dssgtdth.wav",
		act			= "wavhq/dsdmact.wav",
		hit			= "wavhq/dsdmpain.wav",
		melee		= "wavhq/dssgtatk.wav",
	--	hoof		= "wavhq/dshoof.wav";
	},

	-- Cacodemon

	cacodemon = {
		die			= "wavhq/dscacdth.wav",
		act			= "wavhq/dscacsit.wav",
		hit			= "wavhq/dsdmpain.wav",
		melee		= "wavhq/dsclaw.wav",
		fire		= "wavhq/dsfirsht.wav",
		explode		= "wavhq/dsfirxpl.wav",
	},

	-- Arachnotron

	arachno = {
		die			= "wavhq/dsbspdth.wav",
		act			= "wavhq/dsbspact.wav",
		hit			= "wavhq/dsdmpain.wav",
		melee		= "wavhq/dsclaw.wav",
		fire		= "wavhq/dsplasma.wav",
	--	hoof		= "wavhq/dsmetal.wav",
	},

	-- Hell Knight

	knight = {
		die			= "wavhq/dskntdth.wav",
		act			= "wavhq/dskntsit.wav",
		hit			= "wavhq/dsdmpain.wav",
		melee		= "wavhq/dsclaw.wav",
		fire		= "wavhq/dsfirsht.wav",
		explode		= "wavhq/dsfirxpl.wav",
	--	hoof		= "wavhq/dshoof.wav";
	},

	-- Baron of Hell

	baron = {
		die			= "wavhq/dsbrsdth.wav",
		act			= "wavhq/dsbrssit.wav",
		hit			= "wavhq/dsdmpain.wav",
		melee		= "wavhq/dsclaw.wav",
		fire		= "wavhq/dsfirsht.wav",
		explode		= "wavhq/dsfirxpl.wav",
	--	hoof		= "wavhq/dshoof.wav";
	},

	-- Mancubus

	mancubus = {
		die			= "wavhq/dsmandth.wav",
		act			= "wavhq/dsmansit.wav",
		hit			= "wavhq/dsmnpain.wav",
		fire		= "wavhq/dsfirsht.wav",
		explode		= "wavhq/dsfirxpl.wav",
	--	hoof		= "wavhq/dshoof.wav";
	},

	-- Revenant

	revenant = {
		die			= "wavhq/dsskedth.wav",
		act			= "wavhq/dsskesit.wav",
		hit			= "wavhq/dspopain.wav",
		melee		= "wavhq/dsskepch.wav",
		fire		= "wavhq/dsskeatk.wav",
		explode		= "wavhq/dsbarexp.wav",
	--	hoof		= "wavhq/dshoof.wav";
	},

	-- Arch-vile

	arch = {
		die			= "wavhq/dsvildth.wav",
		act			= "wavhq/dsvilact.wav",
		hit			= "wavhq/dsvipain.wav",
		fire		= "wavhq/dsvilatk.wav",
	--	hoof		= "wavhq/dshoof.wav";
	},

	-- Bruiser Brothers

	bruiser = {
		die			= "wavhq/dsbrsdth.wav",
		act			= "wavhq/dsbrssit.wav",
		hit			= "wavhq/dsdmpain.wav",
		melee		= "wavhq/dsclaw.wav",
		fire		= "wavhq/dsfirsht.wav",
		explode		= "wavhq/dsfirxpl.wav",
	--	hoof		= "wavhq/dshoof.wav";
	},

	-- Cyberdemon

	cyberdemon = {
		die			= "wavhq/dscybdth.wav",
		act			= "wavhq/dscybsit.wav",
		hit			= "wavhq/dsdmpain.wav",
		hoof		= "wavhq/dshoof.wav",
	},

	-- JC

	jc = {
		die			= "cc/human-die-1",
		act			= "cc/human-act",
		hit			= "wavhq/dspopain.wav",
		melee		= "cc/human-punch",
	--	hoof		= "wavhq/dshoof.wav";
	},

	-- AoD

	angel = {
		die			= "wavhq/dsbrsdth.wav",
		act			= "wavhq/dsbrssit.wav",
		hit			= "wavhq/dsbrssit.wav",
		melee		= "wavhq/dsclaw.wav",
		hoof		= "wavhq/dshoof.wav";
	},

	-- Mastermind

	mastermind = {
		die			= "wavhq/dsspidth.wav",
		act			= "wavhq/dsdmact.wav",
		hit			= "wavhq/dsdmpain.wav",
		melee		= "wavhq/dsclaw.wav",
		hoof		= "wavhq/dsmetal.wav";
	},

	--
	-- Default sounds
	--

	melee			= "wavhq/dsclaw.wav",
	reload			= "wavhq/dswpnup.wav",
	pickup			= "wavhq/dsitemup.wav",
	fire			= "wavhq/dsfirsht.wav",
	explode			= "wavhq/dsfirxpl.wav",
	powerup			= "wavhq/dsgetpow.wav",
	--]]
}
