/*

###############################################################################
#                                                                             #
#                 LICHEM: Layered Interacting CHEmical Models                 #
#                              By: Eric G. Kratz                              #
#                                                                             #
#                      Symbiotic Computational Chemistry                      #
#                                                                             #
###############################################################################

 Primary functions for LICHEM.

*/

//Core utility functions
void PrintFancyTitle()
{
  cout << '\n';
  cout << "#######################################";
  cout << "########################################";
  cout << '\n';
  cout << "#                                      ";
  cout << "                                       #";
  cout << '\n';
  cout << "#                 ";
  cout << "LICHEM: Layered Interacting CHEmical Models";
  cout << "                 #";
  cout << '\n';
  cout << "#                                      ";
  cout << "                                       #";
  cout << '\n';
  cout << "#                      ";
  cout << "Symbiotic Computational Chemistry";
  cout << "                      #";
  cout << '\n';
  cout << "#                                      ";
  cout << "                                       #";
  cout << '\n';
  cout << "#######################################";
  cout << "########################################";
  cout << '\n' << '\n';
  cout.flush();
  return;
};

double LICHEMFactorial(int n)
{
  //Calculate a factorial
  double val = 1;
  while (n > 0)
  {
    val *= n;
    n -= 1;
  }
  return val;
};

bool CheckFile(const string& file)
{
  //Checks if a file exists
  struct stat buffer;
  if (stat(file.c_str(),&buffer) != -1)
  {
    //Yep...
    return 1;
  }
  //Nope...
  return 0;
};

int FindMaxThreads()
{
  //Function to count the number of allowed threads
  int ct = 0; //Generic counter
  #pragma omp parallel reduction(+:ct)
  ct += 1; //Add one for each thread
  #pragma omp barrier
  //Return total count
  return ct;
};

double Bohring(double ri)
{
  //Convert ri (Bohr) to Angstroms
  double r = 0;
  r = ri/BohrRad;
  return r;
};

Coord CoordDist2(Coord& a, Coord& b)
{
  //Signed displacements
  double dx = a.x-b.x;
  double dy = a.y-b.y;
  double dz = a.z-b.z;
  //Check PBC
  if (PBCon)
  {
    bool check = 1; //Continue checking PBC
    while (check)
    {
      //Overkill, bit it checks if atoms are wrapped multiple times
      check = 0; //Stop if there are no changes
      if (abs(dx) > (0.5*Lx))
      {
        //Update X displacement
        check = 1; //The displacement was updated
        if (dx > 0)
        {
          dx -= Lx;
        }
        else
        {
          dx += Lx;
        }
      }
      if (abs(dy) > (0.5*Ly))
      {
        //Update Y displacement
        check = 1; //The displacement was updated
        if (dy > 0)
        {
          dy -= Ly;
        }
        else
        {
          dy += Ly;
        }
      }
      if (abs(dz) > (0.5*Lz))
      {
        //Update Z displacement
        check = 1; //The displacement was updated
        if (dz > 0)
        {
          dz -= Lz;
        }
        else
        {
          dz += Lz;
        }
      }
    }
  }
  //Save displacements
  Coord DispAB; //Distance between A and B
  DispAB.x = dx;
  DispAB.y = dy;
  DispAB.z = dz;
  return DispAB;
};

//Functions to check connectivity
vector<int> TraceBoundary(vector<QMMMAtom>& Struct, int AtID)
{
  //Function to find all boundary atoms connected to a pseudobond atom
  bool BondError = 0; //Checks if the molecular structure "breaks" the math
  vector<int> BoundAtoms; //Final list of atoms
  //Add atoms bonded to atom "AtID"
  for (unsigned int i=0;i<Struct[AtID].Bonds.size();i++)
  {
    int BondID = Struct[AtID].Bonds[i];
    if (Struct[BondID].BAregion)
    {
      BoundAtoms.push_back(BondID);
    }
    if (Struct[BondID].PBregion and (BondID != AtID))
    {
      //Two PBs are connected and this system will fail
      BondError = 1;
    }
  }
  //Check find other boundary atoms bonded to the initial set
  bool MoreFound = 1; //More boundary atoms were found
  while (MoreFound and (!BondError))
  {
    MoreFound = 0; //Break the loop
    vector<int> tmp;
    for (unsigned int i=0;i<BoundAtoms.size();i++)
    {
      int BAID = BoundAtoms[i];
      for (unsigned int j=0;j<Struct[BAID].Bonds.size();j++)
      {
        int BondID = Struct[BAID].Bonds[j];
        //Check if it is on the list
        bool IsThere = 0;
        for (unsigned int k=0;k<BoundAtoms.size();k++)
        {
          if (BondID == BoundAtoms[k])
          {
            IsThere = 1;
          }
        }
        if (!IsThere)
        {
          if (Struct[BondID].BAregion)
          {
            MoreFound = 1; //Keep going
            tmp.push_back(BondID);
          }
          if (Struct[BondID].PBregion and (BondID != AtID))
          {
            //Two PBs are connected and this system will fail
            BondError = 1;
          }
        }
      }
    }
    //Add them to the list
    for (unsigned int i=0;i<tmp.size();i++)
    {
      bool IsThere = 0;
      for (unsigned int j=0;j<BoundAtoms.size();j++)
      {
        //Avoid adding the atom twice
        if (tmp[i] == BoundAtoms[j])
        {
          IsThere = 1;
        }
      }
      if (!IsThere)
      {
        BoundAtoms.push_back(tmp[i]);
      }
    }
  }
  //Check for errors
  if (BondError)
  {
    cerr << "Error: Two pseudo-bonds are connected through boudary atoms!!!";
    cerr << '\n';
    cerr << " The connections prevent LICHEM from correctly updating";
    cerr << " the charges" << '\n' << '\n';
    cerr.flush();
    //Quit to avoid unphysical results
    exit(0);
  }
  //Return list if there are no errors
  return BoundAtoms;
};

bool Bonded(vector<QMMMAtom>& Struct, int Atom1, int Atom2)
{
  //Function to check if two atoms are 1-2 connected
  bool IsBound = 0;
  for (unsigned int i=0;i<Struct[Atom2].Bonds.size();i++)
  {
    if (Atom1 == Struct[Atom2].Bonds[i])
    {
      IsBound = 1;
    }
  }
  return IsBound;
};

bool Angled(vector<QMMMAtom>& Struct, int Atom1, int Atom3)
{
  //Function to check if two atoms are 1-3 connected
  bool IsBound = 0;
  for (unsigned int i=0;i<Struct[Atom1].Bonds.size();i++)
  {
    int Atom2 = Struct[Atom1].Bonds[i];
    for (unsigned int j=0;j<Struct[Atom2].Bonds.size();j++)
    {
      if (Atom3 == Struct[Atom2].Bonds[j])
      {
        IsBound = 1;
      }
    }
  }
  return IsBound;
};

bool Dihedraled(vector<QMMMAtom>& Struct, int Atom1, int Atom4)
{
  //Function to check if two atoms are 1-4 connected
  bool IsBound = 0;
  for (unsigned int i=0;i<Struct[Atom1].Bonds.size();i++)
  {
    int Atom2 = Struct[Atom1].Bonds[i];
    for (unsigned int j=0;j<Struct[Atom2].Bonds.size();j++)
    {
      int Atom3 = Struct[Atom2].Bonds[j];
      for (unsigned int k=0;k<Struct[Atom3].Bonds.size();k++)
      {
        if (Atom4 == Struct[Atom3].Bonds[k])
        {
          IsBound = 1;
        }
      }
    }
  }
  return IsBound;
};

//Structure correction functions
void PBCCenter(vector<QMMMAtom>& Struct, QMMMSettings& QMMMOpts)
{
  //Move the system to the center of the simulation box
  double avgx = 0;
  double avgy = 0;
  double avgz = 0;
  #pragma omp parallel
  {
    #pragma omp for nowait schedule(dynamic) reduction(+:avgx)
    for (int i=0;i<Natoms;i++)
    {
      //Loop over all beads
      double centx = 0;
      for (int j=0;j<QMMMOpts.Nbeads;j++)
      {
        //Update local average postion
        centx += Struct[i].P[j].x;
      }
      //Upate full average
      avgx += centx;
    }
    #pragma omp for nowait schedule(dynamic) reduction(+:avgy)
    for (int i=0;i<Natoms;i++)
    {
      //Loop over all beads
      double centy = 0;
      for (int j=0;j<QMMMOpts.Nbeads;j++)
      {
        //Update local average postion
        centy += Struct[i].P[j].y;
      }
      //Upate full average
      avgy += centy;
    }
    #pragma omp for nowait schedule(dynamic) reduction(+:avgz)
    for (int i=0;i<Natoms;i++)
    {
      //Loop over all beads
      double centz = 0;
      for (int j=0;j<QMMMOpts.Nbeads;j++)
      {
        //Update local average postion
        centz += Struct[i].P[j].z;
      }
      //Upate full average
      avgz += centz;
    }
  }
  #pragma omp barrier
  //Convert sums to averages
  avgx /= Natoms*QMMMOpts.Nbeads;
  avgy /= Natoms*QMMMOpts.Nbeads;
  avgz /= Natoms*QMMMOpts.Nbeads;
  //Move atoms to the center of the box
  #pragma omp parallel
  {
    #pragma omp for nowait schedule(dynamic)
    for (int i=0;i<Natoms;i++)
    {
      //Loop over all beads
      for (int j=0;j<QMMMOpts.Nbeads;j++)
      {
        //Move bead to the center
        Struct[i].P[j].x -= avgx;
        Struct[i].P[j].x += 0.5*Lx;
      }
    }
    #pragma omp for nowait schedule(dynamic)
    for (int i=0;i<Natoms;i++)
    {
      //Loop over all beads
      for (int j=0;j<QMMMOpts.Nbeads;j++)
      {
        //Move bead to the center
        Struct[i].P[j].y -= avgy;
        Struct[i].P[j].y += 0.5*Ly;
      }
    }
    #pragma omp for nowait schedule(dynamic)
    for (int i=0;i<Natoms;i++)
    {
      //Loop over all beads
      for (int j=0;j<QMMMOpts.Nbeads;j++)
      {
        //Move bead to the center
        Struct[i].P[j].z -= avgz;
        Struct[i].P[j].z += 0.5*Lz;
      }
    }
  }
  #pragma omp barrier
  //Return with updated structure
  return;
};

Coord FindQMCOM(vector<QMMMAtom>& Struct, QMMMSettings& QMMMOpts, int Bead)
{
  //Find the center of mass for the QM region
  Coord QMCOM; //Center of mass position
  double avgx = 0; //Average x position
  double avgy = 0; //Average y position
  double avgz = 0; //Average z position
  double totm = 0; //Total mass
  #pragma omp parallel
  {
    #pragma omp for nowait schedule(dynamic) reduction(+:totm)
    for (int i=0;i<Natoms;i++)
    {
      if (Struct[i].QMregion or Struct[i].PBregion)
      {
        totm += Struct[i].m;
      }
    }
    #pragma omp for nowait schedule(dynamic) reduction(+:avgx)
    for (int i=0;i<Natoms;i++)
    {
      if (Struct[i].QMregion or Struct[i].PBregion)
      {
        avgx += Struct[i].m*Struct[i].P[Bead].x;
      }
    }
    #pragma omp for nowait schedule(dynamic) reduction(+:avgy)
    for (int i=0;i<Natoms;i++)
    {
      if (Struct[i].QMregion or Struct[i].PBregion)
      {
        avgy += Struct[i].m*Struct[i].P[Bead].y;
      }
    }
    #pragma omp for nowait schedule(dynamic) reduction(+:avgz)
    for (int i=0;i<Natoms;i++)
    {
      if (Struct[i].QMregion or Struct[i].PBregion)
      {
        avgz += Struct[i].m*Struct[i].P[Bead].z;
      }
    }
  }
  #pragma omp barrier
  //Save center of mass
  QMCOM.x = avgx/totm;
  QMCOM.y = avgy/totm;
  QMCOM.z = avgz/totm;
  return QMCOM;
};

//Misc.
void PrintLapin()
{
  //Print a nice picture
  stringstream lapin;
  lapin.str("");
  //Add obfuscated text
  lapin << '\n';
  lapin << "                   /^\\";
  lapin << "     /^\\";
  lapin << '\n';
  lapin << "                   |  \\";
  lapin << "   /  |";
  lapin << '\n';
  lapin << "                   |  |";
  lapin << "   |  |";
  lapin << '\n';
  lapin << "                   |";
  lapin << "  |___|  |";
  lapin << '\n';
  lapin << "                  /";
  lapin << "           \\";
  lapin << '\n';
  lapin << "                 /";
  lapin << "   &";
  lapin << "     &";
  lapin << "   \\";
  lapin << '\n';
  lapin << "                 |";
  lapin << "             |";
  lapin << '\n';
  lapin << "                 |";
  lapin << "     .";
  lapin << " .";
  lapin << "     |";
  lapin << '\n';
  lapin << "                  \\";
  lapin << "   \\___/";
  lapin << "   /";
  lapin << '\n';
  lapin << "                   \\_";
  lapin << "       _/";
  lapin << '\n';
  lapin << "                     |";
  lapin << "     |";
  lapin << '\n' << '\n';
  lapin << "         ______";
  lapin << "       ______";
  lapin << "       ______";
  lapin << '\n';
  lapin << "        /";
  lapin << "      \\";
  lapin << "     /";
  lapin << "      \\";
  lapin << "     /";
  lapin << "      \\";
  lapin << '\n';
  lapin << "       /";
  lapin << "        \\";
  lapin << "   /";
  lapin << "        \\";
  lapin << "   /";
  lapin << "        \\";
  lapin << '\n';
  lapin << "      |";
  lapin << "----------";
  lapin << "|";
  lapin << " |";
  lapin << "          |";
  lapin << " |";
  lapin << "**********";
  lapin << "|";
  lapin << '\n';
  lapin << "      [";
  lapin << "          ]";
  lapin << " [";
  lapin << "%%%%%%%%%%";
  lapin << "]";
  lapin << " [";
  lapin << "          ]";
  lapin << '\n';
  lapin << "      |";
  lapin << "----------";
  lapin << "|";
  lapin << " |";
  lapin << "          |";
  lapin << " |";
  lapin << "**********";
  lapin << "|";
  lapin << '\n';
  lapin << "       \\";
  lapin << "        /";
  lapin << "   \\";
  lapin << "        /";
  lapin << "   \\";
  lapin << "        /";
  lapin << '\n';
  lapin << "        \\";
  lapin << "______";
  lapin << "/";
  lapin << "     \\";
  lapin << "______";
  lapin << "/";
  lapin << "     \\";
  lapin << "______";
  lapin << "/";
  lapin << '\n' << '\n' << '\n';
  //Print text and return
  cout << lapin.str();
  cout.flush();
  return;
};

void FetchQuotes(vector<string>& Quotes)
{
  //Generate random quotes
  string dummy; //Generic string
  dummy = "\'It is difficult to prove that this quote is not random.\'";
  dummy += '\n';
  dummy += "                                           -Eric G. Kratz";
  for (int i=0;i<1000;i++)
  {
    //Add quotes to the list
    Quotes.push_back(dummy);
  }
  return;
};

