angular.module('safePet')


.controller('changeController', ['$scope','$state','$stateParams', '$ionicPopup', '$ionicHistory','usersEmailResource', 'dogsResource', 'userInfo', 'socketConn', function($scope,$state, $stateParams, $ionicPopup, $ionicHistory, usersEmailResource, dogsResource, userInfo, socketConn){
	$scope.change = function(user) {
		var confirmAlert = $ionicPopup.confirm({
			title: "Cambiar dueño",
			template: "¿Está seguro que quiere cambiar de dueño a su mascota?"
		}).then(function(res){
			if(res){
				console.log(user.email);
				usersEmailResource.get({email: user.email}, function(usr){
					if(usr.email == userInfo.user.email) {
						var emailAlert = $ionicPopup.alert({
							title: "Email inválido",
							template: "No puedes cambiar de dueño contigo mismo"
						});
					} else {
						console.log("Request dog Change");
						socketConn.emit("requestDog", {dogId: $stateParams.dogId, newOwner: usr._id, oldOwner: userInfo.user._id});
						//Disable Back button
						$ionicHistory.nextViewOptions({
							disableBack: true
						});
						$state.go('app.mainList');
					}
				});
			}
		});
	};
}]);
