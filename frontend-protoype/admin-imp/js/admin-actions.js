// Az admin által elvégezhető ÖSSZES akció - de ezek csak tesztelésre szolgálnak
const actionRouter = ActionRouter.create({
	debug: false,
	actions: {
        logout() {
            if (window.confirm("Biztosan kilépsz?")) {
              console.log("KILÉPÉS");
            }
        },

        // Felhasználó törlése
        del_user(user) {
          console.log("TÖRLÉS: " + user.username);
        },


        // Felhasználó szerkesztése
        edit_user(user) {
          console.log("MÓDOSÍTÁS: " + user.username);
        },


        // Új felhasználó
	}
})



// TESZT ADATOK
var admin_data = {
  "current_user": {
    "id": 2,
    "username": "LeoMinor",
    "description": "Adminisztrátor felhasználó",
    "contact": "sgsgh@asdf.com",
    "is_superuser": true,
    "settings": "",
    "added": "2021-02-21T05:42:02",
    "last_modified": "2021-02-21T05:42:02"
  },
  "users": [
    {
      "id": 1,
      "username": "geer26",
      "description": "Adminisztrátor felhasználó",
      "contact": "none@none.no",
      "is_superuser": true,
      "settings": "",
      "added": "2021-02-21T05:42:02",
      "last_modified": "2021-02-21T05:42:02"
    },
    {
      "id": 2,
      "username": "geer26",
      "description": "Adminisztrátor felhasználó",
      "contact": "none@none.no",
      "is_superuser": true,
      "settings": "",
      "added": "2021-02-21T05:42:02",
      "last_modified": "2021-02-21T05:42:02"
    },
    {
      "id": 3,
      "username": "geer26",
      "description": "Adminisztrátor felhasználó",
      "contact": "none@none.no",
      "is_superuser": true,
      "settings": "",
      "added": "2021-02-21T05:42:02",
      "last_modified": "2021-02-21T05:42:02"
    },
    {
      "id": 4,
      "username": "geer26",
      "description": "Adminisztrátor felhasználó",
      "contact": "none@none.no",
      "is_superuser": true,
      "settings": "",
      "added": "2021-02-21T05:42:02",
      "last_modified": "2021-02-21T05:42:02"
    },
    {
      "id": 5,
      "username": "LeoMinor",
      "description": "Adminisztrátor felhasználó",
      "contact": "sgsgh@asdf.com",
      "is_superuser": true,
      "settings": "",
      "added": "2021-02-21T05:42:02",
      "last_modified": "2021-02-21T05:42:02"
    }
  ],
  "modules": [],
  "modaux": [],
  "testbatteries": [],
  "testsessions": [],
  "clients": [],
  "clientlogs": [],
  "results": []
};
