class ActionRouter {

	constructor(params) {
		this.debug = params.debug == undefined ? false : Boolean(params.debug);

		this.actions = params.actions == undefined ? null : params.actions;
	}

	static create(params) {
		return new ActionRouter(params);
	}

	call(action, param = null) {
		if (this.actions != undefined && this.actions != null && this.actions[action] != undefined && this.actions[action] != null)
			this.actions[action](param);
	}

}