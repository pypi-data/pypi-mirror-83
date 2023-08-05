import re
from typing import List

from rdkit.Chem.fmcs import Atom
from rdkit.Chem.rdchem import Mol, BondType, RWMol, EditableMol
from rdkit.Chem.rdmolfiles import MolToSmiles
from rdkit.Chem.rdmolops import SanitizeMol, CombineMols

from reinvent_chemistry import Conversions, TransformationTokens


class BondMaker:
    def __init__(self):
        self._conversions = Conversions()
        self._tokens = TransformationTokens()

    def join_scaffolds_and_decorations(self, scaffold_smi, decorations_smi):
        decorations_smi = [self.add_first_attachment_point_number(dec, i)
                           for i, dec in enumerate(decorations_smi.split(self._tokens.ATTACHMENT_SEPARATOR_TOKEN))]
        num_attachment_points = len(self.get_attachment_points(scaffold_smi))
        if len(decorations_smi) != num_attachment_points:
            return None

        mol = self._conversions.smile_to_mol(scaffold_smi)
        for decoration in decorations_smi:
            mol = self.join_molecule_fragments(mol, self._conversions.smile_to_mol(decoration))
            if not mol:
                return None
        return mol

    def add_attachment_point_numbers(self, mol_or_smi, canonicalize=True):
        """
        Adds the numbers for the attachment points throughout the molecule.
        :param mol_or_smi: SMILES string to convert.
        :param canonicalize: Canonicalize the SMILES so that the attachment points are always in the same order.
        :return : A converted SMILES string.
        """
        if isinstance(mol_or_smi, str):
            smi = mol_or_smi
            if canonicalize:
                smi = self._conversions.mol_to_smiles(self._conversions.smile_to_mol(mol_or_smi))
            # only add numbers ordered by the SMILES ordering
            num = -1

            def _ap_callback(_):
                nonlocal num
                num += 1
                return "[{}:{}]".format(self._tokens.ATTACHMENT_POINT_TOKEN, num)

            return re.sub(self._tokens.ATTACHMENT_POINT_REGEXP, _ap_callback, smi)
        else:
            mol = mol_or_smi
            if canonicalize:
                mol = self._conversions.smile_to_mol(self._conversions.mol_to_smiles(mol))
            idx = 0
            for atom in mol.GetAtoms():
                if atom.GetSymbol() == self._tokens.ATTACHMENT_POINT_TOKEN:
                    atom.SetProp("molAtomMapNumber", str(idx))
                    idx += 1
            return self._conversions.mol_to_smiles(mol)

    def join_molecule_fragments(self, scaffold, decoration, keep_label_on_atoms=False):
        """
        Joins a RDKit MOL scaffold with a decoration. They must be labelled.
        :param scaffold_smi: RDKit MOL of the scaffold.
        :param decoration_smi: RDKit MOL of the decoration.
        :param keep_label_on_atoms: Add the labels to the atoms after attaching the molecule.
        This is useful when debugging, but it can give problems.
        :return: A Mol object of the joined scaffold.
        """

        if scaffold and decoration:
            # obtain id in the decoration
            try:
                attachment_points = [atom.GetProp("molAtomMapNumber") for atom in decoration.GetAtoms()
                                     if atom.GetSymbol() == self._tokens.ATTACHMENT_POINT_TOKEN]
                if len(attachment_points) != 1:
                    return None  # more than one attachment point...
                attachment_point = attachment_points[0]
            except KeyError:
                return None

            combined_scaffold = RWMol(CombineMols(decoration, scaffold))
            attachments = [atom for atom in combined_scaffold.GetAtoms()
                           if atom.GetSymbol() == self._tokens.ATTACHMENT_POINT_TOKEN and
                           atom.HasProp("molAtomMapNumber") and atom.GetProp("molAtomMapNumber") == attachment_point]
            if len(attachments) != 2:
                return None  # something weird

            neighbors = []
            for atom in attachments:
                if atom.GetDegree() != 1:
                    return None  # the attachment is wrongly generated
                neighbors.append(atom.GetNeighbors()[0])

            bonds = [atom.GetBonds()[0] for atom in attachments]
            bond_type = BondType.SINGLE
            if any(bond for bond in bonds if bond.GetBondType() == BondType.DOUBLE):
                bond_type = BondType.DOUBLE

            combined_scaffold.AddBond(neighbors[0].GetIdx(), neighbors[1].GetIdx(), bond_type)
            combined_scaffold.RemoveAtom(attachments[0].GetIdx())
            combined_scaffold.RemoveAtom(attachments[1].GetIdx())

            if keep_label_on_atoms:
                for neigh in neighbors:
                    self._add_attachment_point_num(neigh, attachment_point)

            # Label the atoms in the bond
            bondNumbers = [int(atom.GetProp("bondNum")) for atom in combined_scaffold.GetAtoms()
                           if atom.HasProp("bondNum")]

            if bondNumbers:
                bondNum = max(bondNumbers) + 1
            else:
                bondNum = 0

            for neighbor in neighbors:
                idx = neighbor.GetIdx()
                atom = combined_scaffold.GetAtomWithIdx(idx)
                atom.SetIntProp("bondNum", bondNum)
            ##########################################

            scaffold = combined_scaffold.GetMol()
            try:
                SanitizeMol(scaffold)
            except ValueError:  # sanitization error
                return None
        else:
            return None

        return scaffold

    def _add_attachment_point_num(self, atom, idx):
        idxs = []
        if atom.HasProp("molAtomMapNumber"):
            idxs = atom.GetProp("molAtomMapNumber").split(",")
        idxs.append(str(idx))
        idxs = sorted(list(set(idxs)))
        atom.SetProp("molAtomMapNumber", ",".join(idxs))

    def get_attachment_points(self, mol_or_smi) -> List:
        """
        Gets all attachment points regardless of the format.
        :param mol_or_smi: A Mol object or a SMILES string
        :return : A list with the numbers ordered by appearance.
        """
        if isinstance(mol_or_smi, Mol):
            return [int(atom.GetProp("molAtomMapNumber")) for atom in mol_or_smi.GetAtoms()
                    if atom.GetSymbol() == self._tokens.ATTACHMENT_POINT_TOKEN and atom.HasProp("molAtomMapNumber")]
        return [int(match.group(1)) for match in re.finditer(self._tokens.ATTACHMENT_POINT_NUM_REGEXP, mol_or_smi)]

    def add_first_attachment_point_number(self, smi, num):
        """
        Changes/adds a number to the first attachment point.
        :param smi: SMILES string with the molecule.
        :param num: Number to add.
        :return: A SMILES string with the number added.
        """
        return re.sub(self._tokens.ATTACHMENT_POINT_REGEXP, "[{}:{}]".format(self._tokens.ATTACHMENT_POINT_TOKEN, num),
                      smi, count=1)

################################################################




    # def join_two_fragments(self, scaffold, decoration):
    #     combined_scaffold = None
    #
    #     if scaffold and decoration:
    #         decoration_attachment = self.get_attachment_point_for_decoration(decoration)
    #         scaff_attachment = self.get_attachment_points_for_scaffold(scaffold, decoration_attachment.GetProp(
    #             "molAtomMapNumber"))
    #         # neighbors = self.get_attachment_point_neighboring_atoms(scaff_attachment, decoration_attachment)
    #         combined_scaffold = RWMol(CombineMols(scaffold, decoration))
    #         attachments = self.get_attachment_points_for_ensemble(combined_scaffold, decoration_attachment.GetProp("molAtomMapNumber"))
    #         neighbors = self.get_attachment_point_neighboring_atoms(attachments[1], attachments[0])
    #
    #         if len(neighbors) == 2:
    #             bond_pair = self._get_indices_from_atom_collection(neighbors)
    #             attachment_indices = self._get_indices_from_atom_collection([scaff_attachment, decoration_attachment])
    #             combined_scaffold = self.form_bonds(combined_scaffold, bond_pair)
    #             combined_scaffold = self.remove_attachment_points(combined_scaffold, attachment_indices)
    #
    #     return combined_scaffold
    #
    # def _update_molecule(self, molecule: Mol):
    #     scaffold = molecule.GetMol()
    #     try:
    #         SanitizeMol(scaffold)
    #     except ValueError:  # sanitization error
    #         return None
    #     return scaffold
    #
    # def get_attachment_point_for_decoration(self, decoration: Mol) -> Atom:
    #     attachment_point = None
    #     try:
    #         attachment_points = [atom for atom in decoration.GetAtoms()
    #                              if atom.GetSymbol() == self._tokens.ATTACHMENT_POINT_TOKEN]
    #         if len(attachment_points) == 1:
    #             attachment_point = attachment_points[0]
    #             # print(type(attachment_point))
    #     except KeyError:
    #         pass
    #     return attachment_point
    #
    # def get_attachment_points_for_scaffold(self, scaffold: Mol, attachment_point: str) -> Atom:
    #     attachments = [atom for atom in scaffold.GetAtoms()
    #                    if atom.GetSymbol() == self._tokens.ATTACHMENT_POINT_TOKEN and
    #                    atom.HasProp("molAtomMapNumber") and atom.GetProp("molAtomMapNumber") == attachment_point]
    #     ############
    #     print("+"*80)
    #     for a in attachments:
    #         print(f'get_attachment_points_for_scaffold {a.GetProp("molAtomMapNumber")} {a.GetIdx()} symbol {a.GetSymbol()}')
    #     ###########
    #     if len(attachments) != 1:
    #         return None
    #     attachment = attachments[0]
    #     return attachment
    #
    # def get_attachment_points_for_ensemble(self, combined_scaffold: Mol, attachment_point: str) -> List[Atom]:
    #     attachments = [atom for atom in combined_scaffold.GetAtoms()
    #                    if atom.GetSymbol() == self._tokens.ATTACHMENT_POINT_TOKEN and
    #                    atom.HasProp("molAtomMapNumber") and atom.GetProp("molAtomMapNumber") == attachment_point]
    #     print("+"*80)
    #     for a in attachments:
    #         print(f'{a.GetProp("molAtomMapNumber")} {a.GetIdx()}')
    #
    #     if len(attachments) != 2:
    #         attachments = []  # something weird
    #     return attachments
    #
    # def get_attachment_point_neighboring_atoms(self, scaffold_attachment, decoration_point) -> List[Atom]:
    #     neighbors = []
    #     if scaffold_attachment.GetDegree() == 1 and decoration_point.GetDegree() == 1:
    #         neighbors = [scaffold_attachment.GetNeighbors()[0], decoration_point.GetNeighbors()[0]]
    #     return neighbors
    #
    # def remove_attachment_points(self, combined_scaffold: Mol, attachments: List[int]) -> Mol:
    #     for index in sorted(attachments, reverse=True):
    #         combined_scaffold.RemoveAtom(index)
    #     return combined_scaffold
    #
    # def form_bonds(self, combined_scaffold: Mol, bond_pairs: List[int]) -> Mol:
    #     combined_scaffold.AddBond(bond_pairs[0], bond_pairs[1], BondType.SINGLE)
    #     return combined_scaffold
    #
    # def _get_indices_from_atom_collection(self, collection: List[Atom]) -> List[int]:
    #     indices = [atom.GetIdx() for atom in collection]
    #     return indices
