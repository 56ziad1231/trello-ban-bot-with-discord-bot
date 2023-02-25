local API = require(game.ServerScriptService:WaitForChild("TrelloAPI"))
local BanBoardId = API:GetBoardID("robloxbans")
local BanListID = API:GetListID("bans",BanBoardId)
local banmsg = 'You are banned from this game'
local servermsgalert = game.ReplicatedStorage:WaitForChild('msgevent')


function checkCurrentPlayersforban()
	while wait(3) do
		local bancards = API:GetCardsInList(BanListID)
		for _, Player in pairs(game.Players:GetChildren()) do
			for _, Card in pairs(bancards) do
				if string.find(Card.name, Player.UserId) then
					servermsgalert:FireAllClients(Player.Name.." Was permanently banned!")
					Player:Kick(banmsg)
					
				end
			end
		end
	end
end

spawn(checkCurrentPlayersforban)

game.Players.PlayerAdded:Connect(function(plr)
	local bancards = API:GetCardsInList(BanListID)
	for _, Card in pairs(bancards) do
		if string.find(Card.name, plr.UserId) then
			print('1')
			plr:Kick('PERMBANNED You are permanently banned from all servers!')
		end
	end
end)
