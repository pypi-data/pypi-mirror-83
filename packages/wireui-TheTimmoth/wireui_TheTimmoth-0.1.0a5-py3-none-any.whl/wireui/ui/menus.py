from .console import print_error
from .console import print_message

from .peers import add_peer
from .peers import delete_peer
from .peers import edit_peer_connections
from .peers import list_peers
from .peers import rekey_peer

from .shared import create_wireguard_config
from .shared import yes_no_menu

from .sites import add_site
from .sites import delete_site
from .sites import get_site_name
from .sites import list_sites

from ..library import WireUI


def start_message():
  print_message(0, "wireui")
  print_message(0, "Tool for creating and managing wireguard configs")
  print_message(0, "Version 0.1.0a")
  print_message(0, "(C) 2020 Tim Schlottmann")
  print_message(0, "")


def entrypoint_menu(w: WireUI):
  while True:
    sites_count = list_sites(w)
    # if sites_count:
    #   print_message(0, "0: List sites")
    print_message(0, "1: Create new site")
    if sites_count:
      print_message(0, "2: Edit existing site")
      print_message(0, "3: Delete existing site")
      print_message(0, "4: Recreate config files")
    print_message(0, "q: Exit")
    choice = input("What do you want to do? ")

    # if choice == "0" and sites_count:
    #   list_sites(w)
    if choice == "1":
      site_menu(w, add_site(w))
    elif choice == "2" and sites_count:
      list_sites(w)
      site_menu(w, get_site_name(w, should_exist=True))
    elif choice == "3" and sites_count:
      list_sites(w)
      delete_site(w)
    elif choice == "4" and sites_count:
      list_sites(w)
      create_wireguard_config(w, get_site_name(w, should_exist=True))
    elif choice == "q":
      _exit(0)

    print_message(0, "")


def site_menu(w: WireUI, site_name: str):
  leave = False
  while not leave:
    peers_count = list_peers(w, site_name)

    # TODO: Remove this hint when editing is possible
    print_message(0,
                  "For full editing of peers please use the sites.json file!")

    # if peers_count:
    #   print_message(0, "0: List peers")
    print_message(0, "1: Add peer")
    if peers_count:
      print_message(0, "2: Create new keys for a peer")
      print_message(0, "3: Delete peer")
      print_message(0, "4: Edit connection table")
    print_message(0, "b: Back")
    print_message(0, "q: Exit")
    choice = input("What do you want to do? ")

    # if choice == "0" and peers_count:
    #   list_peers(w, site_name)
    if choice == "1":
      add_peer(w, site_name)
    elif choice == "2" and peers_count:
      list_peers(w, site_name)
      rekey_peer(w, site_name)
    elif choice == "3" and peers_count:
      list_peers(w, site_name)
      delete_peer(w, site_name)
    elif choice == "4" and peers_count:
      edit_peer_connections(w, site_name)
    elif choice == "b":
      leave = True
    elif choice == "q":
      _exit(0)

    print_message(0, "")


def _exit(i):
  print_message(0, "Bye")
  exit(i)
